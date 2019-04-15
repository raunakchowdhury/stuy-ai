import matplotlib.pyplot as plt

all_words = set()

# Gets all of the words that are the same length as those in the input file
f = open("dictall.txt","r")
for line in f:
    all_words.add(line[:-1])
f.close()

def vowel_const_ratio(word, y_enabled=False):
    # Takes in a word and returns the number of vowels divided by number of consonants
    vowels = set(["a","e","i","o","u"])
    if y_enabled:
        vowels.add('y')
    num_vowel = 0
    for letter in word:
        if letter in vowels:
            num_vowel += 1
    if num_vowel == len(word):
        return -1
    return num_vowel/(len(word)-num_vowel) #Use python3 division

x_arr = [] #length of word
y_arr = [] # vowel to consonant ratio if y is a vowel
y_arr_no_y = [] # vowel to consonant ratio if y isn't a vowel

for word in all_words:
    x_arr.append(len(word))
    y_arr.append(vowel_const_ratio(word,True))
    y_arr_no_y.append(vowel_const_ratio(word))


plt.scatter(x_arr, y_arr)
plt.title('Ratios with y as a vowel')
plt.xlabel('Length of word (in chars)')
plt.ylabel('Vowel:Consanant Ratio')
plt.show()

plt.scatter(x_arr, y_arr_no_y)
plt.title('Ratios with y as not a vowel')
plt.xlabel('Length of word (in chars)')
plt.ylabel('Vowel:Consanant Ratio')
plt.show()

x_axis = [i for i in range(23)]
lowest_ratios = [10] * 23 # Each index contains the lowest ratio for words of length (index + 2)
low_words = [[]] * 23
highest_ratios = [-10] * 23 # Each index contains the highest ratio for words of length (index + 2)
high_words = [[]] * 23
for word in all_words:
    cur_ratio = vowel_const_ratio(word, y_enabled=False)
    length = len(word) - 2
    if cur_ratio < lowest_ratios[length]:
        low_words[length] = []
        low_words[length].append(word)
        lowest_ratios[length] = cur_ratio
    elif cur_ratio == lowest_ratios[length]:
        low_words[length].append(word)
    if cur_ratio > highest_ratios[length]:
        high_words[length] = []
        high_words[length].append(word)
        highest_ratios[length] = cur_ratio
    elif cur_ratio == highest_ratios[length]:
        high_words[length].append(word)

num_low = [len(x) for x in low_words]
num_high = [len(x) for x in high_words]


print("low ratio")
for ratio in lowest_ratios:
    print(ratio)
print("high ratio")
for ratio in highest_ratios:
    print(ratio)
print("low num")
for num in num_low:
    print(num)
print("high num")
for num in num_high:
    print(num)

ratios = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],[]]
all_ratios = []
for word in all_words:
    cur_ratio = vowel_const_ratio(word, y_enabled=True)
    length = len(word) - 2
    ratios[length].append(cur_ratio)
    all_ratios.append(cur_ratio)

def mean(arr):
    sum = 0
    for num in arr:
        sum += num
    avg = sum/len(arr)
    return avg

def mode(arr):
    count = {}
    for num in arr:
        if num not in count.keys():
            count[num] = 1
        else:
            count[num] += 1
    the_mode = -2
    the_count = 0
    for key in count:
        if count[key] > the_count:
            the_mode = key
            the_count = count[key]
    return the_mode

print("means")
means = [mean(x) for x in ratios]
for m in means:
    print(m)

print("\n",mean(all_ratios))

print("modes")
modes = [mode(x) for x in ratios]
for m in modes:
    print(m)

print("\n",mode(all_ratios))

# print(num_low)
# print(num_high)

plt.plot(x_axis, lowest_ratios, label = 'min')
plt.plot(x_axis, highest_ratios, label = 'max')
plt.legend(('Min', 'Max'), loc='upper right')
plt.title('Ratios')
plt.xlabel('Length of word (in chars)')
plt.ylabel('Vowel:Consanant Ratio')
plt.show()
