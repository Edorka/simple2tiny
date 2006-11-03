import string
import re
import sys
from token import Token;
def pos2xy(s, pos):
	linea = len(s[:pos].split('\n'))
	caracter = len(s[:pos].split('\n')[-1:][0])
	return (linea,caracter)
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

		print self.reservadas
		patron = self.registrar()
		self.expr = re.compile(patron, re.VERBOSE)
		self.funciones = {}
		for nombre, id in self.expr.groupindex.items():
			self.funciones[id-1] = getattr( self, 't_' + nombre)
			
	def error(self, s, pos):
		#TODO esto no deberia hacerse aqui, hay que revisar la G.
		linea,caracter = pos2xy(s,pos)
		print "** Error en la linea: "+str(linea)+", columna: "+str(caracter)
		print s.split('\n')[linea-1]
		raise SystemExit		
	
        def expresion(self, nombre):
                doc = getattr(self, nombre).__doc__
                lista = '(?P<%s>%s)' % (nombre[2:], doc)
                return lista
	def registrar(self):
		lista=[]
		for nombre in _namelist(self):
			if nombre[:2] == 't_' and nombre != 't_cadena':
				lista.append(self.expresion(nombre))
		lista.append(self.expresion('t_cadena'))
		return string.join(lista,'|')
        def buscar(self, s):
                pos = 0
		self.lista=[]
                n = len(s)
                while pos < n:
			if s[pos] == '\n' :
				print "->\\n<-"
			else:
				print "->"+s[pos]+"<-"
			m = self.expr.match(s, pos)
			if m is None:
                                self.error(s, pos)
			conjuntos = m.groups()
                        for i in range(len(conjuntos)):
                                if conjuntos[i] and self.funciones.has_key(i):
					self.funciones[i](conjuntos[i],pos2xy(s,pos))
					
                        pos = m.end()
		return self.lista

	def validar(self,entrada):
		self.lista=[]
		Analizador.buscar(self,entrada);
		print self.lista;
		return self.lista

	def t_cadena(self,s,pos):
		r'\".+\"'
		t = Token(type='cadena', attr=s, pos=pos )
		self.lista.append(t)
	def t_cifra_entera(self,s,pos):
		r'(\+|\-)?\d+ (?!\.)' 
		t = Token(type='entero', attr=s, pos=pos)
		self.lista.append(t)

	def t_cifra_entera_h(self,s,pos):
                r'\$(\+|\-)?[0-9,a-f,A-F]+' 
                t = Token(type='entero', attr=s)
                self.lista.append(t)
	def t_real (self,s,pos):
		r'(\+|\-)?\d*\.\d+'
		t =Token(type='real',attr=s)
		self.lista.append(t)
        def t_real_h (self,s,pos):
                r'\$(\+|\-)?([0-9,a-f,A-F])*\.([0-9,a-f,A-F])+'
                t =Token(type='real',attr=s)
                self.lista.append(t)
	def t_identificador(self,s,pos):
		r'[a-z,A-Z] ([a-z,A-Z]|\w)* '
		if s in self.reservadas:
			print "reservada: "+s
			t = Token(type='res', attr=s)
		else:
			print "identificador: "+s
			t = Token(type='id', attr=s)
		self.lista.append(t)
	def t_comentario(self,s,pos):
		r'\/\/(.)*\n'
		pass	
	def t_comentario_multilinea(self,s,pos):
		r'\/\*(.)*\*\/'
		pass
	def t_asignacion(self,s,pos):
		r'(?!\:)='
		self.lista.append(Token(type='asignacion'));
	def t_fin_sentencia(self,s,pos):
		r'(;\n)|;'
		self.lista.append(Token(type='fin_sentencia'))

	def t_fin_linea(self,s,pos):
		r'\n|(\t+\n)'
		self.lista.append(Token(type='fin_linea'))
		print "fin de linea"
		
	def t_espacio (self,s,pos):
		r'\s+'
		pass
	
	def t_llave_i (self,s,pos ):
		r'\{ (?!\*)'
		self.lista.append(Token(type='llave_i'))

        def t_llave_d (self,s,pos):
                r'(?!\*) \}'
		self.lista.append(Token(type='llave_d'))
	
	def t_parentesis_i (self,s,pos):
		r'\( (?!\*)'
		self.lista.append(Token(type='parentesis_i'))

        def t_parentesis_d (self,s,pos):
                r'(?!\*) \)'
		self.lista.append(Token(type='parentesis_d'))

	def t_dospuntos (self,s,pos):
		r':'
		self.lista.append(Token(type='dospuntos'))

        def t_coma(self,s,pos):
	        r','
	        self.lista.append(Token(type='dospuntos'))
        
	def t_operador_suma (self,s,pos):
                r'\+'
                self.lista.append(Token(type='operador_suma'))				
        def t_operador_resta (self,s,pos):
                r'\-'
                self.lista.append(Token(type='operador_resta'))

        def t_operador_mult (self,s,pos):
                r'\*'
                self.lista.append(Token(type='operador_mult'))
        def t_operador_div (self,s,pos):
                r'/(?!/)'
                self.lista.append(Token(type='operador_div'))

if __name__=='__main__':
	f=open(sys.argv[1])
	print "abro "+sys.argv[1]
	analizador = Lexico()
	analizador.buscar( f.read() )
	for a in analizador.lista:
		if a.attr:
			print a.type ,"=>",a.attr
		else:
			print a.type
		if a.pos:
			print "@",a.pos
	print "fin" 
#	def t_operador (self,s,pos):
#		r'\+|\-|\*|/(?!/)'
#		self.lista.append(Token(type='operador',attr=s))
