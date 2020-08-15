# -*- coding: utf-8 -*-
# by digiteng...06.2020, 07.2020,
# <widget source="session.Event_Now" render="xtraBanner" position="0,0" size="762,141" zPosition="1" />
from Renderer import Renderer
from enigma import ePixmap, ePicLoad, eTimer
from Components.AVSwitch import AVSwitch
from Components.Pixmap import Pixmap
from Components.config import config
import re
from Tools.Directories import fileExists

try:
	from Plugins.Extensions.xtraEvent.xtra import xtra
	pathLoc = config.plugins.xtraEvent.loc.value
except:
	pass

class AMB_xtraBanner(Renderer):

	def __init__(self):
		Renderer.__init__(self)

	GUI_WIDGET = ePixmap
	def changed(self, what):
		try:
			if not self.instance:
				return
			
			if what[0] == self.CHANGED_CLEAR:
				self.instance.hide()
			if what[0] != self.CHANGED_CLEAR:
				self.delay()
		except:
			return

	def showBanner(self):
		pstrNm = ""
		event = self.source.event
		try:
			if event:
				evnt = event.getEventName()
				evntNm = re.sub("([\(\[]).*?([\)\]])|(: odc.\d+)|(\d+: odc.\d+)|(\d+ odc.\d+)|(:)|( -(.*?).*)|(,)|!", "", evnt).rstrip()
				pstrNm = "{}xtraEvent/banner/{}.jpg".format(pathLoc, evntNm)
				if fileExists(pstrNm):
					size = self.instance.size()
					self.picload = ePicLoad()
					sc = AVSwitch().getFramebufferScale()
					if self.picload:
						self.picload.setPara((size.width(),
						size.height(),
						sc[0],
						sc[1],
						False,
						1,
						'#00000000'))
					result = self.picload.startDecode(pstrNm, 0, 0, False)
					if result == 0:
						ptr = self.picload.getData()
						if ptr != None:
							self.instance.setPixmap(ptr)
							self.instance.show()
					del self.picload
				else:
					self.instance.hide()
					return
			else:
				self.instance.hide()
				return
		except:
			self.instance.hide()
			return

	def delay(self):
		self.timer = eTimer()
		self.timer.callback.append(self.showBanner)
		self.timer.start(500, True)
