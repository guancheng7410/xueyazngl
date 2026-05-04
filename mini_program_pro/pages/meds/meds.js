const app = getApp()

Page({
  data: {
    currentParent: {},
    medList: [],
    logList: [],
    showModal: false,
    form: { name: '', dosage: '', qty: '30' },
    freqOptions: ['每日1次', '每日2次', '每日3次'],
    freqIndex: 0,
    freqMap: ['once', 'twice', 'thrice']
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

      const meds = wx.getStorageSync('bp_meds_' + pid) || []
      const logs = wx.getStorageSync('bp_logs_' + pid) || []

      const medList = meds.map(m => ({
        ...m,
        daysLeft: m.quantity !== undefined ? Math.floor(m.quantity / (m.times ? m.times.length : 1)) : 99,
        timesStr: (m.times || []).join(', ')
      }))

      const logList = logs.slice().sort((a, b) => a.scheduled < b.scheduled ? 1 : -1).slice(0, 10).map(l => ({
        ...l,
        iconClass: l.status === 'taken' ? 'green' : (l.status === 'missed' ? 'orange' : 'blue'),
        icon: l.status === 'taken' ? '✓' : (l.status === 'missed' ? '✗' : '⏰'),
        statusText: l.status === 'taken' ? '已服' : (l.status === 'missed' ? '漏服' : '待服')
      }))

      this.setData({ medList, logList })
    } catch (e) {
      console.error('加载数据失败', e)
    }
  },

  showAddModal() {
    this.setData({ showModal: true, form: { name: '', dosage: '', qty: '30' }, freqIndex: 0 })
  },

  hideAddModal() {
    this.setData({ showModal: false })
  },

  stopPropagation() {},

  onNameInput(e) { this.setData({ 'form.name': e.detail.value }) },
  onDosageInput(e) { this.setData({ 'form.dosage': e.detail.value }) },
  onQtyInput(e) { this.setData({ 'form.qty': e.detail.value }) },
  onFreqChange(e) { this.setData({ freqIndex: e.detail.value }) },

  addMedication() {
    const { name, dosage, qty } = this.form
    if (!name) { wx.showToast({ title: '请输入药物名称', icon: 'none' }); return }

    const freq = this.freqMap[this.data.freqIndex]
    const defaultTimes = { once: ['08:00'], twice: ['08:00', '18:00'], thrice: ['08:00', '12:00', '20:00'] }
    const times = defaultTimes[freq]

    try {
      const pid = this.data.currentParent.id
      const meds = wx.getStorageSync('bp_meds_' + pid) || []

      meds.push({ id: app.genId(), name, dosage, frequency: freq, times, quantity: parseInt(qty) || 0 })
      wx.setStorageSync('bp_meds_' + pid, meds)

      wx.showToast({ title: '添加成功', icon: 'success' })
      this.hideAddModal()
      this.loadData()
    } catch (e) {
      wx.showToast({ title: '添加失败', icon: 'none' })
    }
  },

  deleteMed(e) {
    const id = e.currentTarget.dataset.id
    wx.showModal({
      title: '确认删除',
      content: '确定删除该药物吗？',
      success: (res) => {
        if (res.confirm) {
          const pid = this.data.currentParent.id
          const meds = wx.getStorageSync('bp_meds_' + pid) || []
          const filtered = meds.filter(m => m.id !== id)
          wx.setStorageSync('bp_meds_' + pid, filtered)
          wx.showToast({ title: '已删除', icon: 'success' })
          this.loadData()
        }
      }
    })
  }
})
