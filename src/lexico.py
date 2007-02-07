#!/usr/bin/python
#-*- coding: iso-8859-15 -*-
# Lexico.py 
# Realizado por: José Antonio Martín Sánchez
# Manuel Jimenez y Eduardo Orive Vinuesa
# Distribuido bajo los terminos de la licencia publica GPL


import string
import re
import sys
from token import Token;

def pos2lc(s, pos):
	linea = len(s[:pos].split('\n'))
	columna = len(s[:pos].split('\n')[-1:][0])
	return (linea,columna)

def _namelist(instance):
	es, directorio,clases  = [], {}, [instance.__class__]
	identificadores = []
	for funcion in dir(instance):
		if not directorio.has_key(funcion):
			identificadores.append(funcion)
			directorio[funcion] = 1
	return identificadores

class Lexico:
	def __init__(self):
		print "inicializando lexico"
		self.reservadas =['class','function','private','public']
		self.reservadas +=['if','for','while']
		self.reservadas +=['void','boolean','integer','float']
		self.reservadas +=['int','real']
		print "registradas ",len(self.reservadas),"palabras reservadas."
		patron = self.registrar()
		print "registrados ",len(patron.split('|')),"patrones."
		self.expr = re.compile(patron, re.VERBOSE)
		self.funciones = {}
		for nombre, id in self.expr.groupindex.items():
			self.funciones[id-1] = getattr( self, 'L_' + nombre)
			
	def error(self, s, pos):
		linea,caracter = pos2lc(s,pos)
		print "** Error en la linea: "+str(linea)+", columna: "+str(caracter)
		print s.split('\n')[linea-1]
		#raise SystemExit		

        def expresion(self, nombre):
                doc = getattr(self, nombre).__doc__
                lista = '(?P<%s>%s)' % (nombre[2:], doc)
                return lista
	def registrar(self):
		lista=[]
		for nombre in _namelist(self):
			if nombre[:2] == 'L_' and nombre != 'L_cadena':
				lista.append(self.expresion(nombre))
		lista.append(self.expresion('L_cadena'))
		return string.join(lista,'|')

        def buscar(self, s):
                pos = 0
		self.lista=[]
                n = len(s)
                while pos < n:
			m = self.expr.match(s, pos)
			if m is None:
                                self.error(s, pos)
				pos += 1 
				continue
			conjuntos = m.groups()
                        for i in range(len(conjuntos)):
                                if conjuntos[i] and self.funciones.has_key(i):
					self.funciones[i](conjuntos[i],pos2lc(s,pos))
                        pos = m.end()
		self.lista.append(Token(type='EOF',pos=pos2lc(s,pos)))
		return self.lista

	def validar(self,entrada):
		self.lista=[]
		Analizador.buscar(self,entrada);
		print self.lista;
		return self.lista

#---------------------- Patrones: --------------------------------
	def L_cadena(self,s,pos):
		r'\".+\"'
		t = Token(type='cadena', attr=s, pos=pos )
		self.lista.append(t)
	def L_cifra_entera(self,s,pos):
		r'(\+|\-)?\d+(?!\.)' 
		t = Token(type='entero', attr=s, pos=pos)
		self.lista.append(t)
	def L_real (self,s,pos):
		r'(\+|\-)?\.\d+E(\+|\-)\d+'
		t =Token(type='real',attr=s, pos=pos)
		self.lista.append(t)
	def L_coma(self,s,pos):
		r'\,'
		self.lista.append(Token(type='coma',pos=pos))
	def L_identificador(self,s,pos):
		r'[a-z,A-Z]((?!(\,|\.))([a-z,A-Z]|\d|\_))* '
		if s in self.reservadas:
			t = Token(type='res', attr=s, pos=pos)
		else:
			t = Token(type='id', attr=s, pos=pos)
		self.lista.append(t)
	def L_comentario(self,s,pos):
		r'\/\/(.)*\n'
		pass	
	def L_comentario_multilinea(self,s,pos):
		r'\/\*(.|\n)*\*\/'
		pass
	def L_nulos(self,s,pos):
		r'\xef|\xbb|\xbf'
		pass
	def L_asignacion(self,s,pos):
		r'(?!(\*|\\|\-))='
		self.lista.append(Token(type='asignacion', pos=pos));
	def L_fin_sentencia(self,s,pos):
		r'(; \n)|;'
		self.lista.append(Token(type='fin_sentencia', pos=pos))
#----------------------- Simbolos -----------------------------------
	def L_fin_linea(self,s,pos):
		r'\n|(\t+\n)'
		self.lista.append(Token(type='fin_linea', pos=pos))
		print "fin de linea"
	def L_espacio (self,s,pos):
		r'(\n|\s)+'
		pass
	def L_llave_i (self,s,pos ):
		r'\{ (?!\*)'
		self.lista.append(Token(type='llave_i', pos=pos))
        def L_llave_d (self,s,pos):
                r'(?!\*) \}'
		self.lista.append(Token(type='llave_d', pos=pos))
	def L_parentesis_i (self,s,pos):
		r'\( (?!\*)'
		self.lista.append(Token(type='parentesis_i', pos=pos))
        def L_parentesis_d (self,s,pos):
                r'(?!\*) \)'
		self.lista.append(Token(type='parentesis_d', pos=pos))
	def L_dospuntos (self,s,pos):
		r':'
		self.lista.append(Token(type='dospuntos', pos=pos))
        def L_coma(self,s,pos):
	        r','
	        self.lista.append(Token(type='coma', pos=pos))
	def L_punto(self,s,pos):
		r'\.(?!\d)'
		self.lista.append(Token(type='punto',pos=pos))
#-------------------------------- Operadores aritmeticos -------------------------        
	def L_operador_suma (self,s,pos):
                r'\+(?!(\.|\d|\+))'
                self.lista.append(Token(type='operador_suma', pos=pos))				
        def L_operador_resta (self,s,pos):
                r'\-(?!(\.|\d|\-))'
                self.lista.append(Token(type='operador_resta', pos=pos))
        def L_operador_mult (self,s,pos):
                r'\*(?!(\/))'
                self.lista.append(Token(type='operador_mult', pos=pos))
        def L_operador_div (self,s,pos):
                r'/(?!/)'
                self.lista.append(Token(type='operador_div', pos=pos))
	def L_operador_inc (self,s,pos):
		r'\+\+(?!(\.|\d))'
		self.lista.append(Token(type='operador_suma', pos=pos))
	def L_operador_dec (self,s,pos):
                r'\-\-(?!(\.|\d))'
		self.lista.append(Token(type='operador_suma', pos=pos))

#-------------------------------- Operadores Logicos ------------------------------
	def L_op_logico_eq(self,s,pos):
		r'\=\='
		self.lista.append(Token(type='op_log_eq', pos=pos))
	def L_op_logico_neq(self,s,pos):
		r'\!\='
		self.lista.append(Token(type='op_log_neq', pos=pos))
	def L_op_logico_geq(self,s,pos):
		r'\>\='
		self.lista.append(Token(type='op_log_geq', pos=pos))
	def L_op_logico_leq(self,s,pos):
		r'\<\='
		self.lista.append(Token(type='op_log_leq', pos=pos))
	def L_op_logico_gt(self,s,pos):
		r'\>'
		self.lista.append(Token(type='op_log_gt', pos=pos))
	def L_op_logico_lt(self,s,pos):
		r'\<'
		self.lista.append(Token(type='op_log_lt', pos=pos))
	def L_op_logico_and(self,s,pos):
		r'\&\&'
		self.lista.append(Token(type='op_log_and', pos=pos))
	def L_op_logico_or(self,s,pos):
		r'\|\|'
		self.lista.append(Token(type='op_log_or', pos=pos))
	def L_op_logico_not(self,s,pos):
		r'\!(?!\=)'
		self.lista.append(Token(type='not', pos=pos))

if __name__=='__main__':
	if len(sys.argv) < 2 :
		print "falta un nombre de fichero como parametro."
		sys.exit(-1)
	for file in sys.argv[1:]:
		print file,
	print "pendientes para analisis lexico."
	analizador = Lexico()
	for file in sys.argv[1:]:	 
		f=open(file)
		print "abro",file
		lista=analizador.buscar( f.read() )
		if lista == 'detenido':
			# algo muy malo ha pasado por aqui
			print "analisis de",file,"detenido."	
			continue
		for a in lista:
			print file,":",
			if a.attr:
				print a.type ,"=>",a.attr,
			else:
				print a.type,
			if a.pos:
				linea,col = a.pos
				print "en linea",linea,"columna",col,
			print "."
		print "fin",file,"pulse intro para continuar" 
		salto =sys.stdin.readline() 
	print "analizados todos los ficheros."
