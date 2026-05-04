const app = getApp()

Page({
  data: {
    currentParent: {},
    members: [],
    collabLogs: [],
    showModal: false,
    form: { name: '', age: '' },
    relations: ['父亲', '母亲', '配偶'],
    relationIndex: 0
  },

  onShow() {
    this.loadData()
  },

  loadData() {
    try {
      const appState = wx.getStorageSync('bp_app_state')
      if (!appState) return

      this.setData({ currentParent: appState.parents.find(p => p.id === appState.pid) || {} })

      const members = appState.parents.map(p => ({
        ...p,
        isCurrent: p.id === appState.pid,
        medCount: (wx.getStorageSync('bp_meds_' + p.id) || []).length
      }))

      const collabLogs = wx.getStorageSync('bp_collab_logs') || []
      this.setData({ members, collabLogs: collabLogs.slice(0, 10) })
    } catch (e) {
      console.error('加载失败', e)
    }
  },

  showAddModal() {
    this.setData({ showModal: true, form: { name: '', age: '' }, relationIndex: 0 })
  },

  hideAddModal() {
    this.setData({ showModal: false })
  },

  stopPropagation() {},

  onNameInput(e) { this.setData({ 'form.name': e.detail.value }) },
  onAgeInput(e) { this.setData({ 'form.age': e.detail.value }) },
  onRelationChange(e) { this.setData({ relationIndex: e.detail.value }) },

  addMember() {
    const { name, age } = this.form
    if (!name || !age) { wx.showToast({ title: '请填写完整信息', icon: 'none' }); return }

    try {
      const appState = wx.getStorageSync('bp_app_state')
      const newId = Date.now()
      const relation = this.data.relations[this.data.relationIndex]
      const gender = relation === '父亲' ? '男' : '女'

      appState.parents.push({ id: newId, name, age: parseInt(age), gender, relation })
      wx.setStorageSync('bp_app_state', appState)
      wx.setStorageSync('bp_meds_' + newId, [])
      wx.setStorageSync('bp_logs_' + newId, [])
      wx.setStorageSync('bp_data_' + newId, [])
      wx.setStorageSync('bp_alerts_' + newId, [])

      wx.showToast({ title: '邀请已发送', icon: 'success' })
      this.hideAddModal()
      this.loadData()
    } catch (e) {
      wx.showToast({ title: '添加失败', icon: 'none' })
    }
  },

  switchParent(e) {
    const pid = e.currentTarget.dataset.id
    if (app.switchParent(pid)) {
      wx.showToast({ title: '已切换', icon: 'success' })
      this.loadData()
    }
  }
})
