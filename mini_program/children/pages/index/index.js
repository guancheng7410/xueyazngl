const app = getApp()

Page({
  data: {
    userInfo: null,
    familyGroups: [],
    currentGroup: null,
    parents: [],
    todayLogs: [],
    activeAlerts: [],
    bpAnalysis: null
  },

  onLoad() {
    this.checkLogin()
  },

  checkLogin() {
    const userInfo = wx.getStorageSync('userInfo')
    if (userInfo) {
      this.setData({ userInfo })
      this.loadFamilyGroups()
    } else {
      this.login()
    }
  },

  login() {
    wx.login({
      success: (res) => {
        if (res.code) {
          wx.request({
            url: 'http://localhost:5000/api/auth/login',
            method: 'POST',
            data: { openid: res.code },
            success: (res) => {
              if (res.data.id) {
                wx.setStorageSync('userInfo', res.data)
                this.setData({ userInfo: res.data })
                this.loadFamilyGroups()
              }
            }
          })
        }
      }
    })
  },

  loadFamilyGroups() {
    wx.request({
      url: 'http://localhost:5000/api/family/groups',
      data: { user_id: this.data.userInfo.id },
      success: (res) => {
        if (res.data.length > 0) {
          this.setData({ familyGroups: res.data })
          this.selectGroup(res.data[0])
        }
      }
    })
  },

  selectGroup(group) {
    this.setData({ currentGroup: group })
    this.loadGroupData()
  },

  loadGroupData() {
    const groupId = this.data.currentGroup.id
    wx.request({
      url: `http://localhost:5000/api/family/groups/${groupId}/parents`,
      success: (res) => {
        this.setData({ parents: res.data })
        if (res.data.length > 0) {
          this.loadTodayLogs(res.data[0].id)
          this.loadBPAnalysis(res.data[0].id)
        }
      }
    })
  },

  loadTodayLogs(parentId) {
    wx.request({
      url: `http://localhost:5000/api/logs/today/${parentId}`,
      success: (res) => {
        this.setData({ todayLogs: res.data })
      }
    })
  },

  loadBPAnalysis(parentId) {
    wx.request({
      url: `http://localhost:5000/api/blood-pressure/analysis/${parentId}`,
      success: (res) => {
        this.setData({ bpAnalysis: res.data })
      }
    })
  },

  onShareAppMessage() {
    return {
      title: '血压守护 - 守护家人健康',
      path: '/pages/index/index'
    }
  }
})
