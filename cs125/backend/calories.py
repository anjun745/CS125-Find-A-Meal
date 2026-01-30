height = 175
weight = 70
gender = 1
age = 20

# calorie predictions:
if gender == 1:  # male
    calories = 10 * weight + 6.25 * height - 5 * age + 5
else:  # female
    calories = 10 * weight + 6.25 * height - 5 * age - 161
