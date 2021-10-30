#!/usr/bin/python3

from flask import Flask, render_template, request
from pickle import load

app = Flask(__name__, template_folder = 'template')

PR = load(open('static/src/Primes', 'rb'))
mx = max(PR)

def miller_rabin(n, k=100):
	if n in range(2, mx):
		if n in PR:
			return True
		else:
			return False
	
	#assert n not multiple of 2
	if n % 2 == 0:
		return False

	k = min(n.bit_length()//10, k)

	# rabin-miller test
	r, s = 0, n - 1
	while s % 2 == 0:
		r += 1
		s //= 2
	for b in range(k):
		x = pow(choice(PR), s, n)
		if x == 1 or x == n - 1:
			continue
		for _ in range(r - 1):
			x = pow(x, 2, n)
			if x == n - 1:
				break
		else:
			return False
	return True

@app.route('/', methods = ["GET", "POST"])
def home():
	out = ""
	if request.method == "POST":
		try:
			val = int(request.form.get('num'))
			if miller_rabin(val):
				out = 'Prime!'
			else:
				out = 'Not a Prime :('
		except:
			out = "Invalid Input!"
	return render_template('index.html', text=out)

if __name__ == '__main__':
	app.run(host="localhost", port=6080)