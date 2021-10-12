
#!/usr/bin/python3

from flask import Flask, render_template, request
import pickle

PR = pickle.load(open('static/src/Primes', 'rb'))
mn, mx = min(PR), max(PR)
app = Flask(__name__, template_folder = 'template')

def miller_rabin(n, b):
	basis = PR[:64]
	# assert n not 2 or 3
	if n == 2 or n == 3:
		return True

	#assert n not multiple of 2
	if n % 2 == 0:
		return False

	# rabin-miller test
	r, s = 0, n - 1
	while s % 2 == 0:
		r += 1
		s //= 2
	for b in basis:
		x = pow(b, s, n)
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
	if request.method == "POST":
		val = int(request.form.get('num'))
		if (val < mx and val in PR) or (val > mx and miller_rabin(n, 64)):
			out = 'Prime!'
		else:
			out = 'Not a Prime :('
		return render_template('index.html', text=out)
	return render_template('index.html')