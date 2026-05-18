class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({
            'amount': amount,
            'description': description
        })

    def withdraw(self, amount, description=""):
        if not self.check_funds(amount):
            return False

        self.ledger.append({
            'amount': -abs(amount),
            'description': description
        })
        return True
        
    def get_balance(self):
        total = 0

        for item in self.ledger:
            total += item['amount']
        return total

    def transfer(self, amount, destination):
        if not self.check_funds(amount):
            return False

        if self.withdraw(amount, f'Transfer to {destination.name}'):
            destination.deposit(amount, f'Transfer from {self.name}')
            return True
        else:
            return False

    def check_funds(self, amount):
        if amount > self.get_balance():
            return False
        else:
            return True

    def __str__(self):
        result = self.name.center(30, "*") + "\n"

        for item in self.ledger:
            description = item['description'][:23]
            amount = f"{item['amount']:.2f}"
            result += f"{description:<23}{amount:>7}\n"

        result += f"Total: {self.get_balance():.2f}"
        return result

def create_spend_chart(categories):
    title = "Percentage spent by category\n"

    spent = []
    
    for category in categories:
        total = 0
        for item in category.ledger:
            if item['amount'] < 0:
                total += -item['amount']

        spent.append(total)

    total_spent = sum(spent)

    percentage = []
    for amount in spent:
        percent = int((amount / total_spent) * 100) // 10 * 10
        percentage.append(percent)

    chart = title
    
    for i in range(100, -1, -10):
        chart += f"{i:>3}|"

        for percent in percentage:
            if percent >= i:
                chart += ' o '
            else:
                chart += '   '
        chart += ' \n'

    chart += '    ' + '-' * (len(categories) * 3 + 1) + '\n'

    max_length = 0
    for category in categories:
        if len(category.name) > max_length:
            max_length = len(category.name)

    for n in range(max_length):
        chart += '     '

        for category in categories:
            if n < len(category.name):
                chart += category.name[n] + '  '
            else:
                chart += '   '
        
        if n < max_length - 1:
            chart += '\n'

    return chart
