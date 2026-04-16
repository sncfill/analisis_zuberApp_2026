import pandas as pd

def astitlestr(self: str) -> str:
		"""Nombre legible de la columna"""
		return self.replace('_', ' ').title()		
def astitle(self: pd.Series) -> pd.Series:
		"""Renombra el Series a un nombre legible"""
		self.name=astitlestr(self.name)
		return self
def rename_series(df: pd.DataFrame, name: str, new_name: str) -> None:
		"""Renombra el Series a un nombre deseado"""
		df.rename(columns = { name : new_name }, inplace = True)

class DecDataFrame:
	"""Decorador de pd.DataFrame"""
	def __init__(self, d: pd.DataFrame):
		if(isinstance(d, pd.Series)):
			self.df = d.to_frame()
		else:
			self.df = d
	"""DataFrame decorado"""
	def __getitem__(self, index) -> pd.Series:
		return self.df[index]
	def __setitem__(self, key, value: pd.Series):
		self.df[key] = value
	def __call__(self) -> pd.DataFrame:
		return self.df
	def __setattr__(self, name, value):
		if(isinstance(value, pd.Series)):
			a = self.__getattribute__(name)
			if(isinstance(a, DecSeries)):
				a.s = value
		else:
			super().__setattr__(name, value)
			if(isinstance(value, DecSeries)):
				if(value._n == ""): # Si NO establecí nombre es porque quiero usar el nombre del atributo como nombre de la columna
					value._n = name
				else: # si establecí nombre...
					if(value._r == True): # Probablemente quiera renombrar la columna con el nombre del atributo
						value.rn(name)
					elif(value._r != False and value._r != ''): # A menos de que quiera darle un nombre diferente
						value.rn(str(value._r))

class DecSeries:
	def __init__(self, parent: DecDataFrame, colname: str = "", rename = True):
		"""
			Decorador de pd.Series.
			Args:
				colname (str): establece el nombre para accesar a column Series en pd.DataFrame
				Si es vacío, establece el nombre de la instancia al momento de crearse en DecDataFrame en el atributo self.n
				rename (any): Si es True (bool) renombra la columna Series pd.DataFrame con el nombre de la instancia creada en DecDataFrame. Si es (string) y diferente a vacío ('') renombra la columna Series pd.DataFrame con el valor asignado
		"""
		if(isinstance(parent, pd.DataFrame)):
			self.p = DecDataFrame(parent)
			"""Parent """
		else:
			self.p = parent
			"""Parent """
		self._n = colname
		"""(Privado) No usar"""
		self._r = rename
		"""(Privado) No usar"""
		
	@property
	def s(self) -> pd.Series:
		"""Obtiene/Establece el pd.Series del pd.DataFrame"""
		return self.p()[self.n]
	@s.setter
	def s(self, value: pd.Series):
		"""Establece el pd.Series del pd.DataFrame"""
		self.p[self._n] = value
	@property
	def n(self) -> str:
		"""Obtiene/Establece el nombre de la columna en pd.DataFrame"""
		return self._n
	@n.setter
	def n(self, value: str):
		"""Obtiene/Establece el nombre de la columna en pd.DataFrame"""
		self._n = value
	def rn(self, new_name: str):
		"""Renombra la columna en pd.DataFrame"""
		self.p.df.rename(columns = { self._n : new_name }, inplace = True)
		self._n = new_name
		return self
	def __call__(self) -> pd.Series:
		return self.p()[self.n]
	def __str__(self) -> str:
			return self.n