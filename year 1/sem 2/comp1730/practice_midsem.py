# QUESTION 1
from statistics import mean

def calculate_average(scores):
    total = sum(scores)
    return total / len(scores)

def get_letter_grade(average):
    rounded = int(average + 0.5)  # round half up to nearest whole number
    if rounded >= 80:
        return "HD"  # High Distinction
    elif rounded >= 70:
        return "D"   # Distinction
    elif rounded >= 60:
        return "CR"   # Credit
    elif rounded >= 50:
        return "P"   # Pass
    else:
        return "N"   # Fail

def main():
    students = [
        ["Alice", [85, 92, 78]],
        ["Bob", [70, 65, 80]],
        ["Charlie", [95, 91, 89]]
    ]

    for name, scores in students:
        avg = calculate_average(scores)
        grade = get_letter_grade(avg)
        print(f"{name}: Average = {avg:.2f}, Grade = {grade}")

if __name__ == "__main__":
    main()


# QUESTION2
def classify_expense(amount, total):
    if amount < 0:
        return None
    percentage = round((amount / total) * 100, 2)

    if percentage > 30:
        return "high"
    elif 10 <= percentage <= 30:
        return "medium"
    else:
        return "low"


def most_expensive(categories, expenses):
    highest_index = 0
    for i in range(1, len(expenses)):
        if expenses[i] > expenses[highest_index]:
            highest_index = i
    return categories[highest_index]


def filter_over_threshold(categories, expenses, threshold):
    result = []
    for i in range(len(categories)):
        if expenses[i] > threshold:
            result.append(categories[i])
    return result


def budget_summary(expenses):
    total = sum(expenses)
    highest = round(max(expenses), 2)
    lowest = round(min(expenses), 2)
    return [total, highest, lowest]

#%%

def test_classify_expense():
    assert classify_expense(40, 100) == "high"
    assert classify_expense(30, 100) == "medium"
    assert classify_expense(20, 100) == "medium"
    assert classify_expense(10, 100) == "medium"
    assert classify_expense(1, 100) == "low"
    assert classify_expense(-1, 100) is None

def test_most_expensive():
    assert most_expensive(["Rent", "Groceries", "Transport", "Utilities", "Entertainment"], [1800, 620, 210, 285, 175]) == "Rent"

def test_filter_over_threshold():
    assert filter_over_threshold(["Rent", "Groceries", "Transport", "Utilities", "Entertainment"], [1800, 620, 210, 285, 175], 600) in (["Rent", "Groceries"], ["Groceries", "Rent"])

def test_budget_summary():
        total, highest_expense, lowest_expense = budget_summary([1800, 620, 210, 285, 175])
        assert abs(total - 3090) < 0.01
        assert highest_expense == 1800
        assert lowest_expense == 175

def test_all():
    test_classify_expense()
    test_most_expensive()
    test_filter_over_threshold()
    test_budget_summary()
    print("All non-hidden tests passed")

if __name__ == "__main__":
    categories = ["Rent", "Groceries", "Transport", "Utilities", "Entertainment"]
    expenses   = [1800, 620, 210, 285, 175]
    #test_all()
