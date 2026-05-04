const app = getApp()

Page({
  data: {
    userInfo: null,
    todayTasks: [],
    parents: [],
    currentParentId: null,
    healthSnapshot: null
  },

  onLoad() {
    this.checkLogin()
  },

  checkLogin() {
    const userInfo = wx.getStorageSync('userInfo')
    if (userInfo) {
      this.setData({ userInfo })
      this.loadTodayTasks()
    } else {
      wx.showToast({ title: '请先登录', icon: 'none' })
    }
  },

  loadTodayTasks() {
    const parentId = this.data.currentParentId || 1
    wx.request({
      url: `http://localhost:5000/api/logs/today/${parentId}`,
      success: (res) => {
        this.setData({ todayTasks: res.data })
      }
    })
  },

  loadHealthSnapshot(parentId) {
    wx.request({
      url: `http://localhost:5000/api/blood-pressure/analysis/${parentId}`,
      success: (res) => {
        this.setData({ healthSnapshot: res.data })
      }
    })
  },

  confirmTask(e) {
    const logId = e.currentTarget.dataset.id
    wx.request({
      url: `http://localhost:5000/api/logs/${logId}/confirm`,
      method: 'POST',
      data: {
        status: 'taken',
        user_id: this.data.userInfo.id
      },
      success: (res) => {
        wx.showToast({ title: '已确认', icon: 'success' })
        this.loadTodayTasks()
      }
    })
  },

  reportAbnormal() {
    wx.showModal({
      title: '异常上报',
      content: '确定要上报异常情况吗？',
      success: (res) => {
        if (res.confirm) {
          wx.showToast({ title: '已上报', icon: 'success' })
        }
      }
    })
  },

  generateHandoverReport() {
    wx.showModal({
      title: '交班小结',
      content: '确定要生成交班小结吗？',
      success: (res) => {
        if (res.confirm) {
          wx.showToast({ title: '已生成交班小结', icon: 'success' })
        }
      }
    })
  }
})
