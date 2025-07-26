from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Loan, Payment
from decimal import Decimal
from .serializers import PaymentSerializer

class LendMoneyView(APIView):
    def post(self, request):
        customer_id = request.data.get("customer_id")
        loan_amount = request.data.get("loan_amount")
        loan_period = request.data.get("loan_period")  # in years
        interest_rate = request.data.get("interest_rate")

        if not all([customer_id, loan_amount, loan_period, interest_rate]):
            return Response(
                {"error": "Missing one or more required fields."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            loan_amount = float(loan_amount)
            loan_period = float(loan_period)
            interest_rate = float(interest_rate)
        except ValueError:
            return Response(
                {"error": "Invalid numeric value."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        total = loan_amount + (loan_amount * interest_rate * loan_period / 100)
        emi = round(total / (loan_period * 12),2)

        loan = Loan.objects.create(
            customer=customer,
            principal_amount=loan_amount,
            interest_rate=interest_rate,
            loan_period_years=loan_period,
            total_amount=total,
            monthly_emi=emi
        )

        return Response(
            {
                "message": "Loan successfully created.",
                "loan_id": str(loan.loan_id),
                "monthly_emi": str(loan.monthly_emi),
                "total_payable": str(loan.total_amount)
            },
            status=status.HTTP_201_CREATED
        )


class MakePaymentView(APIView):
    def post(self, request):
        loan_id = request.data.get("loan_id")
        amount = request.data.get("amount")
        method = request.data.get("payment_method")  # 'EMI' or 'LUMP_SUM'

        # Validate fields
        if not all([loan_id, amount, method]):
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = Decimal(amount)
            loan = Loan.objects.get(loan_id=loan_id)
        except (Loan.DoesNotExist, ValueError, TypeError):
            return Response({"error": "Invalid loan or amount."}, status=status.HTTP_400_BAD_REQUEST)

        # Prevent overpayment
        if amount >= loan.remaining_amount:
            amount = loan.remaining_amount
            loan.remaining_amount = Decimal('0.00')
            loan.status = 'PAID'
            loan.remaining_emi_count = 0
        else:
            loan.remaining_amount -= amount
            if method.upper() == 'EMI':
                loan.remaining_emi_count = max(0, loan.remaining_emi_count - 1)
            else:  # LUMP_SUM
                from math import ceil
                loan.remaining_emi_count = ceil(loan.remaining_amount / loan.monthly_emi)

        # Record the payment
        Payment.objects.create(
            loan=loan,
            amount=amount,
            payment_method=method.upper()
        )

        loan.save()

        return Response(
            {
                "message": "Payment successful.",
                "remaining_amount": str(loan.remaining_amount),
                "remaining_emi_count": loan.remaining_emi_count,
                "status": loan.status
            },
            status=status.HTTP_200_OK
        )

class LoanLedgerView(APIView):
    def get(self, request):
        loan_id = request.query_params.get('loan_id')

        if not loan_id:
            return Response({"error": "Loan ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            loan = Loan.objects.get(loan_id=loan_id)
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found."}, status=status.HTTP_404_NOT_FOUND)

        payments = Payment.objects.filter(loan=loan).order_by('paid_at')
        payment_data = PaymentSerializer(payments, many=True).data

        return Response({
            "loan_id": loan.loan_id,
            "customer": loan.customer.name,
            "transactions": payment_data,
            "remaining_amount": str(loan.remaining_amount),
            "monthly_emi": str(loan.monthly_emi),
            "remaining_emi_count": loan.remaining_emi_count
        }, status=status.HTTP_200_OK)
        
class AccountOverviewView(APIView):
    def get(self, request):
        customer_id = request.query_params.get("customer_id")
        if not customer_id:
            return Response({"error": "Customer ID is required."}, status=400)

        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found."}, status=404)

        loans = Loan.objects.filter(customer=customer)
        data = []

        for loan in loans:
            # Total Interest
            interest = loan.principal_amount * loan.loan_period_years * loan.interest_rate / 100

            # Payments made
            paid = sum(p.amount for p in Payment.objects.filter(loan=loan))

            data.append({
                "loan_id": str(loan.loan_id),
                "principal_amount": float(loan.principal_amount),
                "total_interest": float(interest),
                "total_amount": float(loan.total_amount),
                "monthly_emi": float(loan.monthly_emi),
                "amount_paid_till_date": float(paid),
                "remaining_emi_count": loan.remaining_emi_count
            })

        return Response(data, status=200)