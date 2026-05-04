const app = getApp()

Page({
  data: {
    currentParent: {}
  },

  onShow() {
    try {
      const appState = wx.getStorageSync('bp_app_state')
      if (appState && appState.pid) {
        this.setData({ currentParent: appState.parents.find(p => p.id === appState.pid) || {} })
      }
    } catch (e) {
      console.error('加载数据失败', e)
    }
  },

  loadDemoData() {
    wx.showModal({
      title: '加载演示数据',
      content: '将加载完整的演示数据用于测试，是否继续？',
      success: (res) => {
        if (res.confirm) {
          this.doLoadDemo()
        }
      }
    })
  },

  doLoadDemo() {
    try {
      const uid = 10001, p1 = 10010, p2 = 10011
      const appState = {
        uid, pid: p1, pname: '张大爷',
        parents: [
          { id: p1, name: '张大爷', age: 68, gender: '男', relation: '父亲' },
          { id: p2, name: '李奶奶', age: 65, gender: '女', relation: '母亲' }
        ]
      }
      wx.setStorageSync('bp_app_state', appState)

      const meds = [
        { id: 20001, name: '硝苯地平', dosage: '1片', frequency: 'twice', times: ['08:00', '18:00'], quantity: 5 },
        { id: 20002, name: '阿司匹林', dosage: '100mg', frequency: 'once', times: ['08:00'], quantity: 3 },
        { id: 20003, name: '氨氯地平', dosage: '5mg', frequency: 'once', times: ['20:00'], quantity: 30 }
      ]
      wx.setStorageSync('bp_meds_' + p1, meds)

      const logs = []
      const today = app.todayStr()
      meds.forEach(m => {
        m.times.forEach(t => {
          logs.push({
            id: app.genId(), medId: m.id, medName: m.name, dosage: m.dosage,
            date: today, time: t, scheduled: today + ' ' + t,
            status: t < '10:00' ? 'taken' : 'pending',
            confirmedAt: t < '10:00' ? today + ' ' + t : null
          })
        })
      })
      wx.setStorageSync('bp_logs_' + p1, logs)

      const bps = []
      for (let k = 0; k < 14; k++) {
        const date = app.daysAgo(k)
        bps.push({
          id: app.genId(),
          systolic: 130 + Math.floor(Math.random() * 25),
          diastolic: 80 + Math.floor(Math.random() * 20),
          hr: 65 + Math.floor(Math.random() * 20),
          note: k < 3 ? '晨起' : '睡前',
          time: date + ' 08:' + app.pad(Math.floor(Math.random() * 30))
        })
      }
      bps.sort((a, b) => a.time < b.time ? 1 : -1)
      wx.setStorageSync('bp_data_' + p1, bps)

      const alerts = [
        { id: app.genId(), logId: app.genId(), medName: '硝苯地平', diff: 25, level: 'urgent', status: 'active', time: today + ' 08:25:00' },
        { id: app.genId(), logId: app.genId(), medName: '阿司匹林', diff: 45, level: 'critical', status: 'active', time: today + ' 08:45:00' }
      ]
      wx.setStorageSync('bp_alerts_' + p1, alerts)

      wx.showToast({ title: '加载成功', icon: 'success' })
      this.onShow()
    } catch (e) {
      wx.showToast({ title: '加载失败', icon: 'none' })
    }
  },

  clearAllData() {
    wx.showModal({
      title: '确认清除',
      content: '确定清除所有数据吗？此操作不可恢复！',
      success: (res) => {
        if (res.confirm) {
          try {
            const keys = []
            for (let i = 0; i < wx.getStorageInfoSync().keys.length; i++) {
              const key = wx.getStorageInfoSync().keys[i]
              if (key.indexOf('bp_') === 0) keys.push(key)
            }
            keys.forEach(k => wx.removeStorageSync(k))
            wx.showToast({ title: '已清除', icon: 'success' })
            this.onShow()
          } catch (e) {
            wx.showToast({ title: '清除失败', icon: 'none' })
          }
        }
      }
    })
  }
})
