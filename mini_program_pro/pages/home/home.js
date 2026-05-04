const app = getApp()

Page({
  data: {
    currentParent: {},
    parents: [],
    todayMeds: [],
    todayMedCount: 0,
    completedCount: 0,
    latestBp: '--',
    activeAlerts: [],
    activeAlertCount: 0,
    showSelector: false,
    bpChartData: []
  },

  onLoad() {
    this.loadData()
  },

  onShow() {
    this.loadData()
  },

  loadData() {
    try {
      const appState = wx.getStorageSync('bp_app_state')
      if (!appState || !appState.pid) {
        wx.redirectTo({ url: '/pages/profile/profile' })
        return
      }

      const pid = appState.pid
      this.setData({
        currentParent: appState.parents.find(p => p.id === pid),
        parents: appState.parents
      })

      const meds = wx.getStorageSync('bp_meds_' + pid) || []
      const logs = wx.getStorageSync('bp_logs_' + pid) || []
      const bps = wx.getStorageSync('bp_data_' + pid) || []
      const alerts = wx.getStorageSync('bp_alerts_' + pid) || []

      const today = app.todayStr()
      const todayLogs = logs.filter(l => l.date === today)
      const takenCount = todayLogs.filter(l => l.status === 'taken').length

      const todayMeds = []
      meds.forEach(m => {
        m.times.forEach(t => {
          const log = logs.find(l => l.medId === m.id && l.date === today && l.time === t)
          todayMeds.push({
            id: log ? log.id : app.genId(),
            medId: m.id,
            medName: m.name,
            time: t,
            dosage: m.dosage,
            status: log ? log.status : 'pending'
          })
        })
      })
      todayMeds.sort((a, b) => a.time < b.time ? -1 : 1)

      const latestBp = bps.length > 0 ? bps[0] : null
      const activeAlerts = alerts.filter(a => a.status === 'active')

      this.setData({
        todayMeds,
        todayMedCount: todayLogs.length,
        completedCount: takenCount,
        latestBp: latestBp ? latestBp.systolic + '/' + latestBp.diastolic : '--',
        activeAlerts: activeAlerts.slice(0, 3),
        activeAlertCount: activeAlerts.length,
        bpChartData: bps.slice(0, 7).reverse()
      })

      setTimeout(() => this.drawChart(), 100)
    } catch (e) {
      console.error('加载数据失败', e)
    }
  },

  drawChart() {
    const query = wx.createSelectorQuery()
    query.select('.bp-chart').boundingClientRect()
    query.exec((res) => {
      if (!res[0]) return
      const ctx = wx.createCanvasContext('bpChart', this)
      const width = res[0].width
      const height = res[0].height
      const data = this.data.bpChartData

      if (data.length < 2) return

      const padding = { top: 20, right: 15, bottom: 30, left: 40 }
      const cw = width - padding.left - padding.right
      const ch = height - padding.top - padding.bottom

      const allValues = data.map(d => [d.systolic, d.diastolic]).flat()
      const minVal = Math.floor(Math.min(...allValues) / 10) * 10 - 10
      const maxVal = Math.ceil(Math.max(...allValues) / 10) * 10 + 10

      // Grid
      ctx.setStrokeStyle('#eee')
      ctx.setLineWidth(1)
      for (let i = 0; i <= 4; i++) {
        const y = padding.top + ch * (i / 4)
        ctx.beginPath()
        ctx.moveTo(padding.left, y)
        ctx.lineTo(width - padding.right, y)
        ctx.stroke()
      }

      // Draw line function
      const drawLine = (key, color) => {
        ctx.setStrokeStyle(color)
        ctx.setLineWidth(2)
        ctx.beginPath()
        data.forEach((d, i) => {
          const x = padding.left + (cw / (data.length - 1)) * i
          const y = padding.top + ch * (1 - (d[key] - minVal) / (maxVal - minVal))
          if (i === 0) ctx.moveTo(x, y)
          else ctx.lineTo(x, y)
        })
        ctx.stroke()

        // Points
        ctx.setFillStyle(color)
        data.forEach((d, i) => {
          const x = padding.left + (cw / (data.length - 1)) * i
          const y = padding.top + ch * (1 - (d[key] - minVal) / (maxVal - minVal))
          ctx.beginPath()
          ctx.arc(x, y, 3, 0, Math.PI * 2)
          ctx.fill()
        })
      }

      drawLine('systolic', '#ff5757')
      drawLine('diastolic', '#2196f3')

      ctx.draw()
    })
  },

  confirmMed(e) {
    const logId = e.currentTarget.dataset.id
    const pid = this.data.currentParent.id
    const logs = wx.getStorageSync('bp_logs_' + pid) || []
    const meds = wx.getStorageSync('bp_meds_' + pid) || []

    const log = logs.find(l => l.id == logId)
    if (log) {
      log.status = 'taken'
      log.confirmedAt = new Date().toLocaleString()
      wx.setStorageSync('bp_logs_' + pid, logs)

      const med = meds.find(m => m.id === log.medId)
      if (med && med.quantity !== undefined) {
        med.quantity = Math.max(0, med.quantity - 1)
        wx.setStorageSync('bp_meds_' + pid, meds)
      }

      wx.showToast({ title: '已确认服药', icon: 'success' })
      this.loadData()
    }
  },

  resolveAlert(e) {
    const alertId = e.currentTarget.dataset.id
    const pid = this.data.currentParent.id
    const alerts = wx.getStorageSync('bp_alerts_' + pid) || []

    const alert = alerts.find(a => a.id == alertId)
    if (alert) {
      alert.status = 'resolved'
      wx.setStorageSync('bp_alerts_' + pid, alerts)
      wx.showToast({ title: '预警已处理', icon: 'success' })
      this.loadData()
    }
  },

  showParentSelector() {
    this.setData({ showSelector: true })
  },

  hideParentSelector() {
    this.setData({ showSelector: false })
  },

  switchParent(e) {
    const pid = e.currentTarget.dataset.id
    if (app.switchParent(pid)) {
      wx.showToast({ title: '已切换', icon: 'success' })
      this.setData({ showSelector: false })
      this.loadData()
    }
  },

  goToMeds() {
    wx.switchTab({ url: '/pages/meds/meds' })
  },

  goToBp() {
    wx.switchTab({ url: '/pages/bp/bp' })
  },

  goToAlerts() {
    wx.navigateTo({ url: '/pages/alerts/alerts' })
  }
})
