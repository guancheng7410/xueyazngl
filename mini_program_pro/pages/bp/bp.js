const app = getApp()

Page({
  data: {
    currentParent: {},
    bpList: [],
    showModal: false,
    form: { systolic: '', diastolic: '', hr: '', note: '' },
    avgSys: 0,
    avgDia: 0,
    avgHr: 0,
    status: '',
    statusColor: '#667eea'
  },

  onShow() {
    this.loadData()
  },

  loadData() {
    try {
      const appState = wx.getStorageSync('bp_app_state')
      if (!appState || !appState.pid) return

      const pid = appState.pid
      this.setData({ currentParent: appState.parents.find(p => p.id === pid) })

      const bps = wx.getStorageSync('bp_data_' + pid) || []
      const bpList = bps.slice(0, 15).map(r => {
        const color = r.systolic > 140 ? '#ff5757' : (r.systolic > 130 ? '#ffc107' : '#51cf66')
        const level = r.systolic > 140 ? '偏高' : (r.systolic > 130 ? '正常偏高' : '正常')
        const tagClass = r.systolic > 140 ? 'tag-red' : (r.systolic > 130 ? 'tag-orange' : 'tag-green')
        return { ...r, color, level, tagClass }
      })

      if (bps.length >= 3) {
        const slice = bps.slice(0, 7)
        const avgSys = Math.round(slice.reduce((s, r) => s + r.systolic, 0) / slice.length)
        const avgDia = Math.round(slice.reduce((s, r) => s + r.diastolic, 0) / slice.length)
        const avgHr = Math.round(slice.reduce((s, r) => s + r.hr, 0) / slice.length)
        const status = avgSys > 140 ? '偏高' : (avgSys > 130 ? '正常偏高' : '正常')
        const statusColor = avgSys > 140 ? '#ff5757' : (avgSys > 130 ? '#ffc107' : '#51cf66')
        this.setData({ avgSys, avgDia, avgHr, status, statusColor })
      }

      this.setData({ bpList })
    } catch (e) {
      console.error('加载数据失败', e)
    }
  },

  showAddModal() {
    this.setData({
      showModal: true,
      form: { systolic: '', diastolic: '', hr: '', note: '' }
    })
  },

  hideAddModal() {
    this.setData({ showModal: false })
  },

  stopPropagation() {},

  onSystolicInput(e) {
    this.setData({ 'form.systolic': e.detail.value })
  },

  onDiastolicInput(e) {
    this.setData({ 'form.diastolic': e.detail.value })
  },

  onHrInput(e) {
    this.setData({ 'form.hr': e.detail.value })
  },

  onNoteInput(e) {
    this.setData({ 'form.note': e.detail.value })
  },

  addBpRecord() {
    const { systolic, diastolic, hr, note } = this.form
    const sys = parseInt(systolic)
    const dia = parseInt(diastolic)
    const heartRate = parseInt(hr) || 72

    if (!sys || !dia) {
      wx.showToast({ title: '请输入血压值', icon: 'none' })
      return
    }
    if (sys < 70 || sys > 250 || dia < 40 || dia > 150) {
      wx.showToast({ title: '血压值不在正常范围', icon: 'none' })
      return
    }

    try {
      const pid = this.data.currentParent.id
      const bps = wx.getStorageSync('bp_data_' + pid) || []
      const now = new Date()
      const timeStr = now.getFullYear() + '-' + app.pad(now.getMonth() + 1) + '-' + app.pad(now.getDate()) + ' ' + app.pad(now.getHours()) + ':' + app.pad(now.getMinutes())

      const record = {
        id: app.genId(),
        systolic: sys,
        diastolic: dia,
        hr: heartRate,
        note: note,
        time: timeStr
      }

      bps.unshift(record)
      bps.sort((a, b) => a.time < b.time ? 1 : -1)
      wx.setStorageSync('bp_data_' + pid, bps)

      wx.showToast({ title: '记录成功', icon: 'success' })
      this.hideAddModal()
      this.loadData()
    } catch (e) {
      console.error('保存失败', e)
      wx.showToast({ title: '保存失败', icon: 'none' })
    }
  }
})
