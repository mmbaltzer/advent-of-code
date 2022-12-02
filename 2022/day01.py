
foodlist = open('2022/data/foodlist.txt','r')

calories_by_elf = [0]
n = 0
for line in foodlist.readlines():
  if line != '\n':
    calories_by_elf[n] += int(line)
  else:
    n += 1
    calories_by_elf.append(0)

calories_by_elf.sort(reverse=True)

# part a
print(max(calories_by_elf))
# part b
print(sum(calories_by_elf[0:3]))