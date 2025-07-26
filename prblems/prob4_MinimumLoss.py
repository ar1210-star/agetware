def minimize_loss(prices):
    n = len(prices)
    min_loss = float('inf')
    buy_year = sell_year = -1

    for i in range(n):
        for j in range(i + 1, n):  
            if prices[j] < prices[i]:
                loss = prices[i] - prices[j]
                if loss < min_loss:
                    min_loss = loss
                    buy_year = i + 1 
                    sell_year = j + 1

    if buy_year == -1:
        print("No valid loss found")
    else:
        print(f"Buy in year {buy_year}, sell in year {sell_year}, loss = {min_loss}")

print("Enter stocks year wise from 1 to n")
stock_list = [int(i) for i in input().split()]
minimize_loss(stock_list)