import sys
import re

if len(sys.argv) <= 1 or sys.argv[1] == "":
	print "Please, enter an equation as an argument."
	equ = raw_input("\n\033[1mEquation\033[0m: ")
else:
	equ = sys.argv[1]
	print "\n\033[1mEquation\033[0m:", equ

s_equ = equ.split('=') # equation simplifiee, s_equ[0] = partie gauche de l'egal, s_equ[1] = partie droite

if len(s_equ) != 2:
	print 'Please, enter a valid equation as an argument.'
	sys.exit(0)

total = [[], [], []] # left, right, total

# le tri
j = 0
for part in s_equ:
	index = s_equ.index(part)
	list = re.findall(r"[\w.+-]+", s_equ[s_equ.index(part)])
	s_equ[index] = list
	i = 0
	n = 0
	for elem in s_equ[index]:
		if elem == 'X':
			if i == (len(s_equ[index]) - 1) or list[i + 1] == '+' or list[i + 1] == '-':
				n = 1
			elif int(list[i + 1]) > n:
				n = int(list[i + 1])
		i += 1;
	i = 0
	while n > -1:
		total[index].append(0)
		n -= 1
	for elem in s_equ[index]:
		if (i == 0 or list[i - 1] == '+' or list[i - 1] == '-') and (i == (len(s_equ[index]) - 1) or list[i + 1] == '+' or list[i + 1] == '-'):
			power = 0
			coef = float(elem)
			total[j][power] = coef
		elif elem == 'X':
			if list[i - 2] == '-':
				list[i - 1] = '-' + list[i - 1]
			if list[i - 1] == '+' or list[i - 1] == '-':
				coef = 1
			else:
				coef = float(list[i - 1])
			if i == (len(s_equ[index]) - 1) or list[i + 1] == '+' or list[i + 1] == '-':
				power = 1
			else:
				power = int(list[i + 1])
			total[j][power] = coef
		i += 1
	j += 1

def ft_sqrt(nb):
	a = 0.0
	b = 0.0
	m = 0.0
	xn = 0.0
	if nb == 0.0:
		return 0.0
	else:
		m = 1.0
		xn = nb
		while xn >= 2.0:
			xn = 0.25 * xn
			m = 2.0 * m
		while xn < 0.50:
			xn = 4.0 * xn
			m = 0.50 * m
		a = xn
		b = 1.0 - xn
		a = a * (1.0 + 0.50 * b)
		b = 0.25 * (3.0 + b) * b * b
		while b >= 1.0E-15:
			a = a * (1.0 + 0.50 * b)
			b = 0.25 * (3.0 + b) * b * b
		return a * m

# si les left et right ne sont pas de meme lg
if len(total[0]) < len(total[1]):
	while len(total[0]) < len(total[1]):
		total[0].append(0)
elif len(total[0]) > len(total[1]):
	while len(total[0]) > len(total[1]):
		total[1].append(0)

# la somme
for i in range(len(total[1])):
	total[2].append(total[0][i] - total[1][i])

# le tableau text_coef pour l'affichage textuel, mais utiliser total[2] pour recuperer les coef en nb
i = 0
text_coef = []
for coef in total[2]:
	if i == 0:
		text_coef.append(str(coef)) # juste pour eviter que le + soit en debut d'equation
	elif coef < 0 and total[2][i - 1] == 0:
		coef *= -1
		text_coef.append(' -' + str(coef) + ' * X^' + str(i))
	elif coef < 0:
		coef *= -1
		text_coef.append(' - ' + str(coef) + ' * X^' + str(i))
	elif coef > 0 and total[2][i - 1] == 0 and (i - 1) == 0:
		text_coef.append(str(coef) + ' * X^' + str(i))
	elif coef > 0:
		text_coef.append(' + ' + str(coef) + ' * X^' + str(i))
	i += 1

def degree_calc():
	deg = len(total[2]) - 1
	while deg > 0:
		if total[2][deg] != 0:
			return deg
		deg -= 1
	return 0 #IL FAUT RESOUDRE LE PROBLEME DE PUISSANCES

degree = degree_calc()

if len(text_coef) == 1 and text_coef[0] == '0.0':
	print "\033[1mReduced form\033[0m: 0 = 0\n"
	print "Every number of R is solution of this equation."
elif degree == 0 and len(total[2]) == 1 and total[2][0] == 0:
	print "Every number of R is solution of this equation."
if degree == 0 and len(total[2]) == 1 and total[2][0] != 0:
	red = ""
	for coef in text_coef:
		if coef != '0' and coef != '0.0':
			red += coef
	print "\033[1mReduced form\033[0m: %s = 0\n" % red
	print "There is no solution to this equation."
elif degree == -1:
	print "Please, enter a valid equation as an argument."
elif degree >= 1:
	red = ""
	for coef in text_coef:
		if coef != '0' and coef != '0.0':
			red += coef
	print "\033[1mReduced form\033[0m: %s = 0\n" % red
	print "This is an \033[1mequation of \033[33mdegree %d\033[0m.\n" % degree

# fonction de resolution, pour degres de 0 a 2
def resolution(degree):
	if degree == 1:
		b = total[2][0]
		a = total[2][1]
		sol = (-b/a)
		if sol == -0:
			sol = 0
		print "\033[1mThe only solution\033[0m is:"
		print "\t\033[31m s = -b/a\033[0m"
		print "\t\033[31m   = %d/%d\033[0m" % (-b, a)
		print "\t\033[31m   = %.5f\033[0m" % sol
	elif degree == 2:
		c = total[2][0]
		b = total[2][1]
		a = total[2][2]
		disc = (b ** 2) - (4 * a * c)
		print "The \033[1mdiscriminant d\033[0m equals:"
		print "\t\033[32md = b^2 - 4ac\n\t  = %s^2 - 4 * %s * %s\n\t  = %s\033[0m\n" % (str(b) if b > 0 else '(' + str(b) + ')', str(a) if a > 0 else '(' + str(a) + ')', str(c) if c > 0 else '(' + str(c) + ')', str(disc))
		if disc > 0:
			sol1 = (-b + (disc ** 0.5))/(2 * a)
			sol2 = (-b - (disc ** 0.5))/(2 * a)
			if sol1 == -0:
				sol1 = 0
			if sol2 == -0:
				sol2 = 0
			print "As the discriminant is \033[1mstrictly positive, the two solutions\033[0m are :"
			print "\t\033[31m\033[1ms1\033[0m\033[31m = (-b + Vd) / 2a \t\t\t\t \033[1ms2\033[0m\033[31m = (-b - Vd) / 2a\033[0m"
			print "\t\033[31m   = (%d + V%d) / (2 * %d) \t\t\t    = (%d - V%d) / (2 * %d)\033[0m" % (-b, disc, a, -b, disc, a)
			print "\t\033[31m   = %.5f \t\t\t\t\t    = %.5f\033[0m" % (sol1, sol2)
		elif disc == 0:
			sol0 = -b/(2 * a)
			print "As the discriminant is \033[1mnull, the solution\033[0m is :"
			print "\t\033[31m s = -b / (2 * a)\033[0m"
			print "\t\033[31m   = %d / (2 * %d)\033[0m" % (-b, a)
			print "\t\033[31m   = %.5f\033[0m" % sol0
		else:
			disc *= -1
			solpart1 = -b/(2 * a)
			solpart2 = (disc ** 0.5)/(2 * a)
			if solpart1 == 0:
				print "As the discriminant is \033[1mstrictly negative, the two solutions\033[0m are:"
				print "\t\033[31ms1 = (-b + iVd)/2a \t\t\t s2 = (-b - iVd)/2a"
				print "\t   = %.5fi \t\t\t   = -%.5fi\033[0m" % (solpart2, solpart2)
			else:
				print "As the discriminant is \033[1mnegative, the two solutions\033[0m are (with V being the square root):"
				print "\t\033[31m\033[1ms1\033[0m\033[31m = (-b + iVd) / 2a \t\t\t\t \033[1ms2\033[0m\033[31m = (-b - iVd) / 2a\033[0m"
				print "\t\033[31m   = (%d + i * V%d) / (2 * %d) \t\t\t    = (%d - i * V%d) / (2 * %d)\033[0m" % (-b, disc, a, -b, disc, a)
				print "\t\033[31m   = %d / (2 * %d) + ((i * V%d) / (2 * %d)) \t    = %d / (2 * %d) - ((i * V%d) / (2 * %d))\033[0m" % (-b, a, disc, a, -b, a, disc, a)
				print "\t\033[31m   = %.5f + %.5f\033[1mi\033[0m\033[31m \t\t\t    = %.5f - %.5f\033[1mi\033[0m" % (solpart1, solpart2, solpart1, solpart2)

if degree > 2:
	print "The polynomial degree is stricly greater than 2, I can't solve it. Sorry :("
elif degree == 0 or degree == 1 or degree == 2:
	resolution(degree)
