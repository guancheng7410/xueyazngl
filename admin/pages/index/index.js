const app = getApp()

Page({
  data: {
    stats: {
      totalUsers: 0,
      totalFamilies: 0,
      totalMedications: 0,
      activeAlerts: 0
    },
    recentAlerts: [],
    systemHealth: 'normal'
  },

  onLoad() {
    this.checkAdmin()
  },

  checkAdmin() {
    const userInfo = wx.getStorageSync('userInfo')
    if (!userInfo || userInfo.role !== 'admin') {
      wx.showToast({ title: '无权限访问', icon: 'none' })
      return
    }
    this.setData({ userInfo })
    this.loadDashboard()
  },

  loadDashboard() {
    wx.request({
      url: 'http://localhost:5000/api/admin/dashboard',
      success: (res) => {
        if (res.data) {
          this.setData({ stats: res.data.stats })
          this.setData({ recentAlerts: res.data.recent_alerts })
        }
      }
    })
  },

  viewUser(userId) {
    wx.navigateTo({
      url: `/pages/user-detail/index?userId=${userId}`
    })
  },

  viewAlert(alertId) {
    wx.navigateTo({
      url: `/pages/alert-detail/index?alertId=${alertId}`
    })
  }
})
