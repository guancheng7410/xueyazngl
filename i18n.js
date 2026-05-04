/**
 * 血压守护 - 多语言支持（i18n）
 * 支持中文、英文、日文
 */

var i18n = {
    currentLang: 'zh',
    defaultLang: 'zh',

    translations: {
        zh: {
            // 导航
            home: '首页',
            meds: '药物',
            bp: '血压',
            alerts: '预警',
            family: '家庭',
            profile: '我的',

            // 首页
            todayMedCount: '今日服药',
            completed: '已完成',
            latestBp: '最新血压',
            bpTrend: '📊 血压趋势（近7天）',
            todayMedPlan: '💊 今日服药计划',
            alertCenter: '🔔 预警中心',
            familyMembers: '👨‍👩‍👧 家庭成员',
            viewAll: '查看全部',
            viewDetails: '详情',
            all: '全部',
            manage: '管理',

            // 药物
            myMeds: '我的药物',
            addMed: '+ 添加',
            medLog: '服药记录',
            medName: '药物名称',
            dosage: '剂量',
            frequency: '服药频次',
            medTimes: '服药时间',
            inventory: '库存数量',
            save: '保存',
            cancel: '取消',
            delete: '删除',
            confirm: '确认',
            sufficient: '充足',
            lowStock: '库存不足',
            daysLeft: '剩余{0}天',
            taken: '已服',
            missed: '漏服',
            pending: '待服',

            // 血压
            bpRecords: '血压记录',
            addBpRecord: '+ 记录',
            systolic: '收缩压（mmHg）',
            diastolic: '舒张压（mmHg）',
            heartRate: '心率（次/分钟）',
            note: '备注',
            healthAssessment: '📊 健康评估',
            normal: '正常',
            highNormal: '正常偏高',
            high: '偏高',
            avgBp: '平均血压',
            avgHr: '平均心率',
            healthStatus: '健康状态',
            recordDays: '记录天数',

            // 预警
            alertList: '预警列表',
            pushSettings: '🔔 推送通知设置',
            enablePush: '启用推送通知',
            level1Alert: '一级预警（分钟）',
            level2Alert: '二级预警（分钟）',
            level3Alert: '紧急预警（分钟）',
            alertSaved: '预警设置已保存',
            active: '未处理',
            resolved: '已处理',
            resolve: '处理',
            overtime: '超时{0}分钟',
            urgent: '重要',
            critical: '紧急',
            warn: '预警',

            // 家庭
            addMember: '+ 邀请',
            switchParent: '切换查看对象',
            collabLog: '协作日志',
            memberName: '姓名',
            relation: '关系',
            age: '年龄',
            father: '父亲',
            mother: '母亲',
            spouse: '配偶',
            current: '当前',
            sendInvite: '发送邀请',

            // 个人
            dataExport: '📊 导出数据',
            loadDemo: '📋 加载演示数据',
            syncData: '🔄 同步数据',
            clearData: '🗑️ 清除所有数据',
            about: '关于',
            version: '版本：{0}',
            familyRole: '家庭成员({0}人)',

            // 通用
            confirmDelete: '确定删除该药物吗？',
            confirmClear: '确定清除所有数据吗？此操作不可恢复！',
            medAdded: '药物添加成功',
            medDeleted: '药物已删除',
            medConfirmed: '已确认服药',
            bpRecorded: '血压记录成功',
            alertResolved: '预警已处理',
            dataExported: '数据已导出',
            demoLoaded: '演示数据加载成功',
            dataCleared: '数据已清除',
            settingsSaved: '设置已保存',
            enterMedName: '请输入药物名称',
            enterMedTime: '请设置服药时间',
            enterBpValue: '请输入血压值',
            bpOutOfRange: '血压值不在正常范围',
            enterName: '请输入姓名',
            enterAge: '请输入年龄',
            noMeds: '暂无药物',
            noBp: '暂无血压记录',
            noAlerts: '暂无预警',
            noCollabLog: '暂无协作日志',
            syncSuccess: '数据同步成功',
            syncLocal: '使用本地数据',

            // 报告
            healthReport: '🩺 血压守护 - 健康报告',
            reportDate: '报告日期：',
            dataOverview: '📊 数据概览',
            bpTrendChart: '📈 血压趋势图',
            bpDistribution: '🩺 血压分布',
            medStats: '💊 服药统计',
            bpDetails: '📋 血压记录详情',
            exportPDF: '📄 导出PDF报告',
            exportImage: '🖼️ 导出图片',
            back: '← 返回',
            generatedBy: '本报告由系统自动生成，仅供参考'
        },

        en: {
            // Navigation
            home: 'Home',
            meds: 'Meds',
            bp: 'BP',
            alerts: 'Alerts',
            family: 'Family',
            profile: 'Profile',

            // Home
            todayMedCount: 'Today\'s Meds',
            completed: 'Completed',
            latestBp: 'Latest BP',
            bpTrend: '📊 BP Trend (7 Days)',
            todayMedPlan: '💊 Today\'s Med Plan',
            alertCenter: '🔔 Alert Center',
            familyMembers: '👨‍👩‍👧 Family Members',
            viewAll: 'View All',
            viewDetails: 'Details',
            all: 'All',
            manage: 'Manage',

            // Meds
            myMeds: 'My Medications',
            addMed: '+ Add',
            medLog: 'Medication Log',
            medName: 'Medication Name',
            dosage: 'Dosage',
            frequency: 'Frequency',
            medTimes: 'Medication Times',
            inventory: 'Inventory',
            save: 'Save',
            cancel: 'Cancel',
            delete: 'Delete',
            confirm: 'Confirm',
            sufficient: 'Sufficient',
            lowStock: 'Low Stock',
            daysLeft: '{0} days left',
            taken: 'Taken',
            missed: 'Missed',
            pending: 'Pending',

            // BP
            bpRecords: 'BP Records',
            addBpRecord: '+ Record',
            systolic: 'Systolic (mmHg)',
            diastolic: 'Diastolic (mmHg)',
            heartRate: 'Heart Rate (bpm)',
            note: 'Note',
            healthAssessment: '📊 Health Assessment',
            normal: 'Normal',
            highNormal: 'High Normal',
            high: 'High',
            avgBp: 'Avg BP',
            avgHr: 'Avg Heart Rate',
            healthStatus: 'Health Status',
            recordDays: 'Record Days',

            // Alerts
            alertList: 'Alert List',
            pushSettings: '🔔 Push Notification',
            enablePush: 'Enable Push',
            level1Alert: 'Level 1 Alert (min)',
            level2Alert: 'Level 2 Alert (min)',
            level3Alert: 'Critical Alert (min)',
            alertSaved: 'Alert settings saved',
            active: 'Active',
            resolved: 'Resolved',
            resolve: 'Resolve',
            overtime: '{0} min overdue',
            urgent: 'Urgent',
            critical: 'Critical',
            warn: 'Warning',

            // Family
            addMember: '+ Invite',
            switchParent: 'Switch Member',
            collabLog: 'Collaboration Log',
            memberName: 'Name',
            relation: 'Relation',
            age: 'Age',
            father: 'Father',
            mother: 'Mother',
            spouse: 'Spouse',
            current: 'Current',
            sendInvite: 'Send Invite',

            // Profile
            dataExport: '📊 Export Data',
            loadDemo: '📋 Load Demo Data',
            syncData: '🔄 Sync Data',
            clearData: '🗑️ Clear All Data',
            about: 'About',
            version: 'Version: {0}',
            familyRole: 'Family ({0} members)',

            // Common
            confirmDelete: 'Are you sure to delete this medication?',
            confirmClear: 'Are you sure to clear all data? This cannot be undone!',
            medAdded: 'Medication added',
            medDeleted: 'Medication deleted',
            medConfirmed: 'Medication confirmed',
            bpRecorded: 'BP recorded',
            alertResolved: 'Alert resolved',
            dataExported: 'Data exported',
            demoLoaded: 'Demo data loaded',
            dataCleared: 'Data cleared',
            settingsSaved: 'Settings saved',
            enterMedName: 'Please enter medication name',
            enterMedTime: 'Please set medication time',
            enterBpValue: 'Please enter BP value',
            bpOutOfRange: 'BP value out of range',
            enterName: 'Please enter name',
            enterAge: 'Please enter age',
            noMeds: 'No medications',
            noBp: 'No BP records',
            noAlerts: 'No alerts',
            noCollabLog: 'No collaboration log',
            syncSuccess: 'Data synced',
            syncLocal: 'Using local data',

            // Report
            healthReport: '🩺 BP Guardian - Health Report',
            reportDate: 'Report Date: ',
            dataOverview: '📊 Data Overview',
            bpTrendChart: '📈 BP Trend Chart',
            bpDistribution: '🩺 BP Distribution',
            medStats: '💊 Medication Stats',
            bpDetails: '📋 BP Records',
            exportPDF: '📄 Export PDF',
            exportImage: '🖼️ Export Image',
            back: '← Back',
            generatedBy: 'This report is auto-generated for reference only'
        },

        ja: {
            // Navigation
            home: 'ホーム',
            meds: '薬',
            bp: '血圧',
            alerts: '警告',
            family: '家族',
            profile: 'プロフィール',

            // Home
            todayMedCount: '今日の薬',
            completed: '完了',
            latestBp: '最新血圧',
            bpTrend: '📊 血圧トレンド（7日間）',
            todayMedPlan: '💊 今日の服薬計画',
            alertCenter: '🔔 警告センター',
            familyMembers: '👨‍👩‍👧 家族メンバー',
            viewAll: 'すべて表示',
            viewDetails: '詳細',
            all: 'すべて',
            manage: '管理',

            // Meds
            myMeds: '私の薬',
            addMed: '+ 追加',
            medLog: '服薬記録',
            medName: '薬の名前',
            dosage: '用量',
            frequency: '頻度',
            medTimes: '服薬時間',
            inventory: '在庫',
            save: '保存',
            cancel: 'キャンセル',
            delete: '削除',
            confirm: '確認',
            sufficient: '十分',
            lowStock: '在庫不足',
            daysLeft: '残り{0}日',
            taken: '服用済み',
            missed: '服用忘れ',
            pending: '未服用',

            // BP
            bpRecords: '血圧記録',
            addBpRecord: '+ 記録',
            systolic: '収縮期血圧（mmHg）',
            diastolic: '拡張期血圧（mmHg）',
            heartRate: '心拍数（bpm）',
            note: 'メモ',
            healthAssessment: '📊 健康評価',
            normal: '正常',
            highNormal: 'やや高め',
            high: '高め',
            avgBp: '平均血圧',
            avgHr: '平均心拍数',
            healthStatus: '健康状態',
            recordDays: '記録日数',

            // Alerts
            alertList: '警告リスト',
            pushSettings: '🔔 プッシュ通知',
            enablePush: '通知を有効にする',
            level1Alert: 'レベル1警告（分）',
            level2Alert: 'レベル2警告（分）',
            level3Alert: '緊急警告（分）',
            alertSaved: '警告設定が保存されました',
            active: '未処理',
            resolved: '処理済み',
            resolve: '処理',
            overtime: '{0}分経過',
            urgent: '重要',
            critical: '緊急',
            warn: '警告',

            // Family
            addMember: '+ 招待',
            switchParent: 'メンバー切替',
            collabLog: 'コラボログ',
            memberName: '名前',
            relation: '関係',
            age: '年齢',
            father: '父',
            mother: '母',
            spouse: '配偶者',
            current: '現在',
            sendInvite: '招待を送信',

            // Profile
            dataExport: '📊 データエクスポート',
            loadDemo: '📋 デモデータ読込',
            syncData: '🔄 データ同期',
            clearData: '🗑️ 全データ削除',
            about: 'について',
            version: 'バージョン：{0}',
            familyRole: '家族（{0}人）',

            // Common
            confirmDelete: 'この薬を削除しますか？',
            confirmClear: 'すべてのデータを削除しますか？元に戻せません！',
            medAdded: '薬が追加されました',
            medDeleted: '薬が削除されました',
            medConfirmed: '服薬確認済み',
            bpRecorded: '血圧が記録されました',
            alertResolved: '警告が処理されました',
            dataExported: 'データがエクスポートされました',
            demoLoaded: 'デモデータが読み込まれました',
            dataCleared: 'データが削除されました',
            settingsSaved: '設定が保存されました',
            enterMedName: '薬の名前を入力してください',
            enterMedTime: '服薬時間を設定してください',
            enterBpValue: '血圧値を入力してください',
            bpOutOfRange: '血圧値が範囲外です',
            enterName: '名前を入力してください',
            enterAge: '年齢を入力してください',
            noMeds: '薬がありません',
            noBp: '血圧記録がありません',
            noAlerts: '警告がありません',
            noCollabLog: 'コラボログがありません',
            syncSuccess: 'データ同期完了',
            syncLocal: 'ローカルデータ使用中',

            // Report
            healthReport: '🩺 血圧ガード - 健康レポート',
            reportDate: 'レポート日付：',
            dataOverview: '📊 データ概要',
            bpTrendChart: '📈 血圧トレンド',
            bpDistribution: '🩺 血圧分布',
            medStats: '💊 服薬統計',
            bpDetails: '📋 血圧記録',
            exportPDF: '📄 PDFエクスポート',
            exportImage: '🖼️ 画像エクスポート',
            back: '← 戻る',
            generatedBy: 'このレポートは自動生成された参考用です'
        }
    },

    /**
     * 设置语言
     * @param {string} lang - 'zh' | 'en' | 'ja'
     */
    setLang: function(lang) {
        if (this.translations[lang]) {
            this.currentLang = lang;
            localStorage.setItem('bp_lang', lang);
            this.applyTranslations();
        }
    },

    /**
     * 获取翻译文本
     * @param {string} key - 翻译键
     * @param {...string} args - 格式化参数
     * @returns {string} 翻译后的文本
     */
    t: function(key) {
        var text = (this.translations[this.currentLang] || this.translations.zh)[key] || key;
        var args = Array.prototype.slice.call(arguments, 1);
        args.forEach(function(arg, i) {
            text = text.replace('{' + i + '}', arg);
        });
        return text;
    },

    /**
     * 应用翻译到页面
     */
    applyTranslations: function() {
        var self = this;
        document.querySelectorAll('[data-i18n]').forEach(function(el) {
            var key = el.getAttribute('data-i18n');
            el.textContent = self.t(key);
        });
        document.querySelectorAll('[data-i18n-placeholder]').forEach(function(el) {
            var key = el.getAttribute('data-i18n-placeholder');
            el.placeholder = self.t(key);
        });
        document.documentElement.lang = this.currentLang === 'zh' ? 'zh-CN' : this.currentLang;
    },

    /**
     * 初始化语言设置
     */
    init: function() {
        var savedLang = localStorage.getItem('bp_lang');
        if (savedLang && this.translations[savedLang]) {
            this.currentLang = savedLang;
        } else {
            var browserLang = navigator.language || navigator.userLanguage;
            if (browserLang.startsWith('en')) {
                this.currentLang = 'en';
            } else if (browserLang.startsWith('ja')) {
                this.currentLang = 'ja';
            } else {
                this.currentLang = 'zh';
            }
        }
    }
};

// 初始化语言
i18n.init();
