# -*- coding: utf-8 -*-

"""
Based on an algorithm by Lepage 1998 ('Solving analogies on words: an algorithm', 
In Proceedings of COLING-ACL’98, Vol 1, pages 728–735, Montreal, August 1998). 

It solves the problem of ordering components of the solution of an analogical proportion 
(x), by proceeding through the matching of a and b/c from left to right, alternating b and 
c each time a match is found, and returning a value for x when everything in a has been 
matched.

It has the following limitations:
1. It only works for flat sequences, and cannot accomodate hierarchical structure
(e.g. it cannot alter part of a feature bundle, or insert something into a syllable)
2. It makes the assumption that all shared elements between the input and the output
will maintain their order (e.g. it cannot reverse segments in a word).

CHANGES
• altered (8/6/2016) to add final word boundary symbol, which
is a fix for a problem where it gives solutions like Repauka : Repauko: = 
Rebasileuka : Rebo:sileuka (effectively running an a -> o: rule on the wrong a)
• 24/11/2020: converted to Python 3
• January 2021: Fixed a bug

"""
from __future__ import print_function
	
def find_first_match(a, b, log=False):
	"""
	Finds the shared subsequence between a and b which is earliest in a, and extends it as far as 
	possible. Returns material before and after the match in a and b. Raises ValueError
	if no match can be found.
	"""
	if log: print("matching %r and %r" % (a, b))
	match = ""
	matched = False
	new_a = ['','']
	for i in range(len(a)):
		if a[i] in b:
			match = a[i]
			break
		else: new_a[0] += a[i]
	if not match: 
		raise ValueError('%r has no matches with %r' % (a, b))
	for j in range(i+1, len(a)):
		if not matched and match + a[j] in b: 
			match += a[j]
		else: 
			matched = True
			new_a[1] += a[j]
	index = b.index(match)
	new_b = [b[:index],b[index+len(match):]]
	if log: print("Match:", match)
	return (new_a, new_b)
	

def find_x(a, b, c, log=False):
	def compute_x(a, b, c, log=False):
		"""
		Runs matching algorithm on b and c alternately, each time:
		• deleting matched material from sources (a and b/c),
		• assigning anything in b/c which precedes the match to x,
		• reassigning b/c to whatever follows the match.
		When everything in a has been matched, adds what remains of b/c to x and returns
		result.	If any subsequence of a cannot be located in b or c, a ValueError is raised.
		"""
		x = ""
		while a != "":	
			try: y,z = find_first_match(a, b, log)
			except ValueError: raise ValueError('Ill-formed (Cannot match %r and %r)' % (a, b))
			if log: print(y, z)
			if y[0] != '': raise ValueError('Ill-formed (Cannot match %r and %r)' % (a, b))
			a = y[1]
			x += z[0]
			b = z[1]
			if log: print('Current values: a: %r, b: %r, c: %r, x: %r' % (a, b, c, x))
			b, c = c, b	
			if log: print('(Switching b with c)\n')
		if log: print("Result:", x+b+c, "\n")
		return x+b
	"""
	Adding final word boundary
	"""
	def add_boundaries(str): return "^"+str+"$"
	def remove_boundaries(str):	return str[1:-1]
	a, b, c = add_boundaries(a), add_boundaries(b), add_boundaries(c)	
	"""
	Reversing strings
	"""
	def reverse(string): return string[::-1]
	"""
	Running compute_x. If it raises a ValueError the first time, tries switching b & c. 
	If this still doesn't work, it tries running on reversed strings.
	"""
	try: return remove_boundaries(compute_x(a, b, c, log))
	except ValueError: 
		try: return remove_boundaries(compute_x(a, c, b, log))
		except ValueError:
			a, b, c = reverse(a), reverse(b), reverse(c)
			try: return reverse(remove_boundaries(compute_x(a, b, c, log)))
			except ValueError:
				return reverse(remove_boundaries(compute_x(a, c, b, log)))
		
	

"""Well-formedness tests"""
assert find_x('animus', 'animi:','sena:tus') == 'sena:ti:'
assert find_x('animī', 'animus','senātī') == 'senātus'			
assert find_x('pepaukamen', 'pepauka:si', 'elipomen') == 'elipo:si'
assert find_x('duck', 'duckling','dump') == 'dumpling'			
assert find_x('ebion','ebiosan','elthon') == 'elthosan'			# insertion
assert find_x('cat', 'crat', 'cog') == 'crog'					# insertion where a and c don't share word final sequence
assert find_x('cat', 'crat', 'bat') == 'brat'					# insertion where a and c don't share word initial sequence
assert find_x('make', 'remake', 'gloat') == 'regloat'			# prefixation
assert find_x('dogs','dog','cats') == 'cat' 					# deletion (from word end)
assert find_x('hear', 'ear','heye') == 'eye'					# deletion (word initial)
assert find_x('cart', 'cat','mart') == 'mat'					# deletion (word internal)
assert find_x('cat', 'bec', 'batge') == 'bebge'					# deletion of suffix and addition of prefix
assert find_x('abc', 'cba', 'abd') == 'dba' 					# deletion of prefix and addition of suffix
assert find_x('cat', 'becontso', 'badge') 	== 'bebondgeso' 	# prefixation, ablaut, and suffixation
assert find_x('cat', 'ag', 'cit') == 'ig'						# deletion of prefix and suffix, addition of suffix
assert find_x('abc', 'acd', 'dbf') == 'dfd'						# deletion of infix, addition of suffix
assert find_x('ustom', 'itom', 'grabus')   == 'grabi' 			# location of material to be changed differs in a and c
assert find_x('bobe', 'baba', 'tote') == 'tata'					# discontinuous marking					
assert find_x('drive', 'drove','dive') == 'dove'				# ablaut
assert find_x('pepauka', 'pepauka:si','epausa')  == 'epausa:si'	# a is a subsequence of b
assert find_x('cat', 'cats', 'scat') == 'scats' 				# a is a subsequence of b and c
assert find_x('dog', 'dogs', 'cat')  == 'cats'					# a and c have no segments in common
assert find_x('dog', 'cat', 'dogs')  == 'cats'					# a and b have no segments in common
print("Well-formedness tests passed")


"""Ill-formedness tests"""
# Canonically ill-formed: not all segments of a can be matched in either b or c
try: 
	find_x('animus', 'animi:', 'princeps')	
	raise ValueError('Should not have passed')		
except ValueError as e: pass					
try: 
	find_x('animus', 'animi:', 'caput')	
	raise ValueError('Should not have passed')		
except ValueError as e: pass
try: 
	find_x('a', 'b', 'c')
	raise ValueError('Should not have passed')		
except ValueError as e: pass
# The following require a more sophisticated matching mechanism than given here; it needs 
# to recognise e.g. that 'b' in 'bog' and 'c' in 'cat' share the feature of being an
# initial segment. 
try: 
	find_x('cat', 'crat', 'bog')
	raise ValueError('Should not have passed')		
except ValueError as e: pass			
try: 
	find_x('cat', 'cra', 'tot') 	
	raise ValueError('Should not have passed')		
except ValueError as e: pass
try: 
	find_x('abc', 'cba', 'def')	
	raise ValueError('Should not have passed')			
except ValueError as e: pass
print("Ill-formedness tests passed")
