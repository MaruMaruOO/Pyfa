import wx
from service.fit import Fit

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.helpers import InternalCommandHistory
from gui.fitCommands.calc.implant.remove import CalcRemoveImplantCommand


class GuiRemoveImplantsCommand(wx.Command):

    def __init__(self, fitID, positions):
        wx.Command.__init__(self, True, 'Remove Implants')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.positions = positions

    def Do(self):
        results = []
        for position in sorted(self.positions, reverse=True):
            cmd = CalcRemoveImplantCommand(fitID=self.fitID, position=position)
            results.append(self.internalHistory.submit(cmd))
        success = any(results)
        eos.db.flush()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        eos.db.flush()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
