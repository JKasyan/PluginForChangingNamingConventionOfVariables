import sublime
import sublime_plugin
import re

class ChangeVarStyleCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		select = view.sel()
		if len(select) and not select[0].empty():
			ch = ChangeVarStyle()
			selected_as_str = view.substr(select[0])
			ch.setStrategy(checkStrategy(selected_as_str))
			if selected_as_str:
				result = ch.change(selected_as_str)
				print(result)
				view.replace(edit, select[0], result)

def checkStrategy(row):
	if '_' in row:
		return ChangeUnderscoreOnUppercaseStrategy()
	else:
		return ChangeUppercaseOnUnderscoreStrategy()

class ChangeUppercaseOnUnderscoreStrategy:

	def change(self,row_as_str):
		split_row = split_by_uppercase(row_as_str, '[A-Z][^A-Z]*')
		res = None
		pos = 0
		for each_word in split_row:
			if not pos:
			  res = each_word.lower()
			else:
			  res += '_' + each_word.lower()
			pos += 1
		return res

class ChangeUnderscoreOnUppercaseStrategy:

	def change(self, row_as_str):
		return row_as_str.title().replace('_', '')

class ChangeVarStyle:

	strategy = None

	def setStrategy(self, strategy):
		self.strategy = strategy

	def change(self, row_as_str):
		return self.strategy.change(row_as_str)
