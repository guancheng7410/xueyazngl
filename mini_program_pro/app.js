App({
  globalData: {
    userInfo: null,
    currentParent: null,
    API_BASE: 'https://your-api-domain.com/api'
  },

  onLaunch() {
    // 检查更新
    if (wx.canIUse('getUpdateManager')) {
      const updateManager = wx.getUpdateManager()
      updateManager.onCheckForUpdate(function (res) {
        if (res.hasUpdate) {
          updateManager.onUpdateReady(function () {
            wx.showModal({
              title: '更新提示',
              content: '新版本已经准备好，是否重启应用？',
              success(res) {
                if (res.confirm) updateManager.applyUpdate()
              }
            })
          })
        }
      })
    }

    // 加载本地数据
    this.loadLocalData()

    // 请求通知权限
    this.requestNotification()
  },

  loadLocalData() {
    try {
      const appState = wx.getStorageSync('bp_app_state')
      if (appState) {
        this.globalData.currentParent = appState.parents.find(p => p.id === appState.pid)
      }
    } catch (e) {
      console.error('加载本地数据失败', e)
    }
  },

  requestNotification() {
    if (wx.canIUse('authorize')) {
      wx.authorize({
        scope: 'scope.setting',
        success() {},
        fail() {}
      })
    }
  },

  switchParent(parentId) {
    try {
      const appState = wx.getStorageSync('bp_app_state')
      const parent = appState.parents.find(p => p.id === parentId)
      if (parent) {
        appState.pid = parentId
        appState.pname = parent.name
        wx.setStorageSync('bp_app_state', appState)
        this.globalData.currentParent = parent
        return true
      }
    } catch (e) {
      console.error('切换失败', e)
    }
    return false
  },

  pad(n) {
    return n < 10 ? '0' + n : '' + n
  },

  todayStr() {
    const d = new Date()
    return d.getFullYear() + '-' + this.pad(d.getMonth() + 1) + '-' + this.pad(d.getDate())
  },

  daysAgo(n) {
    const d = new Date()
    d.setDate(d.getDate() - n)
    return d.getFullYear() + '-' + this.pad(d.getMonth() + 1) + '-' + this.pad(d.getDate())
  },

  genId() {
    return Date.now() + Math.floor(Math.random() * 10000)
  }
})
