class XLSFile:
	def __init__(self, fname=None, b64=None):
		self._gc = GlobalContext();
		self.c = PyV8.JSContext(self._gc);
		self.c.enter();
		self.c.eval(xlsjscode);
		if fname is not None: self.readfile(fname);
		elif b64 is not None: self.readb64(b64);

	def sheetnames(self, idx=None):
		"""Returns an array of the sheet names"""
		if idx is None: return self.wb.SheetNames[:]
		return self.wb.SheetNames[idx]

	def sheet(self, idx_or_name):
		"""Returns a sheet object given an index or name"""
		if isinstance(idx_or_name, int):
			return self.sheet(self.sheetnames(idx_or_name));
		return XLSSheet(self.wb.Sheets[idx_or_name]);

	def readb64(self, b64):
		self.wb = self.c.locals['XLS'].read(b64, {'type': 'base64'});
		return self.wb;

	def readfile(self, fname):
		return self.readb64(base64.b64encode(open(fname, 'rb').read()));

	def csvify(self, sheet):
		return self.c.locals['XLS'].utils.sheet_to_csv(sheet.ws if isinstance(sheet, XLSSheet) else sheet);

