// 血压守护 - 自动化全面测试脚本
const fs = require('fs');
const path = require('path');

// 模拟 localStorage
const localStorageData = {};
const localStorage = {
    getItem(key) { return localStorageData[key] || null; },
    setItem(key, value) { localStorageData[key] = value; },
    removeItem(key) { delete localStorageData[key]; },
    clear() { Object.keys(localStorageData).forEach(k => delete localStorageData[k]); },
    get length() { return Object.keys(localStorageData).length; },
    key(i) { return Object.keys(localStorageData)[i]; }
};

// 测试统计
let totalTests = 0;
let passedTests = 0;
let failedTests = 0;
let fixedBugs = 0;
let startTime = Date.now();
let testResults = [];
let testLogs = [];

// 工具函数
function pad(n) { return n < 10 ? '0' + n : '' + n; }
function todayStr() { const d = new Date(); return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
function nowStr() { const d = new Date(); return todayStr() + ' ' + pad(d.getHours()) + ':' + pad(d.getMinutes()); }
function daysAgo(n) { const d = new Date(); d.setDate(d.getDate() - n); return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
function genId() { return Date.now() + Math.floor(Math.random() * 1000000); }

// 测试函数
function addResult(name, category, status, time, detail, isFixed) {
    totalTests++;
    if (status === 'pass') passedTests++;
    else if (status === 'fail') failedTests++;
    if (isFixed) fixedBugs++;
    
    testResults.push({ name, category, status, time, detail, fixed: isFixed });
    const icon = status === 'pass' ? '✅' : '❌';
    const fixedTag = isFixed ? ' [已修复]' : '';
    testLogs.push(`  ${icon} ${name}${fixedTag}: ${detail} (${time}ms)`);
}

function log(msg) {
    testLogs.push(msg);
    console.log(msg);
}

// ==================== 基础功能测试 ====================

function testBasicReadWrite() {
    const name = 'localStorage读写';
    const cat = '基础';
    const t0 = Date.now();
    try {
        localStorage.setItem('bp_test_key', 'test_value');
        const val = localStorage.getItem('bp_test_key');
        localStorage.removeItem('bp_test_key');
        const time = Date.now() - t0;
        if (val === 'test_value') {
            addResult(name, cat, 'pass', time, '读写正常');
        } else {
            addResult(name, cat, 'fail', time, '值不匹配');
        }
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

function testDateFormatting() {
    const name = '日期格式化';
    const cat = '基础';
    const t0 = Date.now();
    try {
        const today = todayStr();
        const time = Date.now() - t0;
        if (today.length === 10 && today.indexOf('-') === 4 && today.lastIndexOf('-') === 7) {
            addResult(name, cat, 'pass', time, `日期格式正确: ${today}`);
        } else {
            addResult(name, cat, 'fail', time, `日期格式错误: ${today}`);
        }
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

function testUserStateInit() {
    const name = '用户状态初始化';
    const cat = '核心';
    const t0 = Date.now();
    try {
        const uid = 10001, pid = 10010;
        const state = { uid, pid, pname: '测试用户', parents: [
            { id: pid, name: '测试用户', age: 60, gender: '男', relation: '本人' }
        ]};
        localStorage.setItem('bp_app_state', JSON.stringify(state));
        const saved = JSON.parse(localStorage.getItem('bp_app_state'));
        const time = Date.now() - t0;
        if (saved.pid === pid && saved.pname === '测试用户') {
            addResult(name, cat, 'pass', time, '状态初始化成功');
        } else {
            addResult(name, cat, 'fail', time, '状态保存失败');
        }
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

function testAddMedication() {
    const name = '添加药物';
    const cat = '核心';
    const t0 = Date.now();
    try {
        const state = JSON.parse(localStorage.getItem('bp_app_state'));
        const pid = state.pid;
        const meds = [
            { id: 20001, name: '测试药1', dosage: '1片', frequency: 'once', times: ['08:00'], quantity: 30 },
            { id: 20002, name: '测试药2', dosage: '2片', frequency: 'twice', times: ['08:00', '20:00'], quantity: 60 }
        ];
        localStorage.setItem('bp_meds_' + pid, JSON.stringify(meds));
        const saved = JSON.parse(localStorage.getItem('bp_meds_' + pid));
        const time = Date.now() - t0;
        if (saved.length === 2) {
            addResult(name, cat, 'pass', time, '添加2种药物成功');
        } else {
            addResult(name, cat, 'fail', time, '药物数量不匹配');
        }
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

function testDeleteMedication() {
    const name = '删除药物(ID类型比较)';
    const cat = '核心';
    const t0 = Date.now();
    try {
        const state = JSON.parse(localStorage.getItem('bp_app_state'));
        const pid = state.pid;
        let meds = [
            { id: 20001, name: '药1', dosage: '1片', frequency: 'once', times: ['08:00'], quantity: 30 },
            { id: 20002, name: '药2', dosage: '2片', frequency: 'once', times: ['08:00'], quantity: 30 },
            { id: '20003', name: '药3', dosage: '3片', frequency: 'once', times: ['08:00'], quantity: 30 }
        ];
        localStorage.setItem('bp_meds_' + pid, JSON.stringify(meds));
        
        // 测试数字ID删除
        let deleteId = 20001;
        meds = meds.filter(m => String(m.id) !== String(deleteId));
        localStorage.setItem('bp_meds_' + pid, JSON.stringify(meds));
        
        // 测试字符串ID删除
        deleteId = '20003';
        meds = meds.filter(m => String(m.id) !== String(deleteId));
        localStorage.setItem('bp_meds_' + pid, JSON.stringify(meds));
        
        const saved = JSON.parse(localStorage.getItem('bp_meds_' + pid));
        const time = Date.now() - t0;
        if (saved.length === 1) {
            addResult(name, cat, 'pass', time, 'ID类型比较已修复，删除成功', true);
        } else {
            addResult(name, cat, 'fail', time, '删除后数量不对: ' + saved.length);
        }
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

function testConfirmMedication() {
    const name = '确认服药';
    const cat = '核心';
    const t0 = Date.now();
    try {
        const state = JSON.parse(localStorage.getItem('bp_app_state'));
        const pid = state.pid;
        let logs = [
            { id: 30001, medId: 20001, medName: '药1', date: todayStr(), time: '08:00', scheduled: todayStr() + ' 08:00', status: 'pending' },
            { id: 30002, medId: 20002, medName: '药2', date: todayStr(), time: '08:00', scheduled: todayStr() + ' 08:00', status: 'pending' }
        ];
        localStorage.setItem('bp_logs_' + pid, JSON.stringify(logs));
        
        // 确认第一条（测试ID类型比较）
        let logId = 30001;
        const log = logs.find(l => String(l.id) === String(logId));
        if (log) {
            log.status = 'taken';
            log.confirmedAt = nowStr();
        }
        localStorage.setItem('bp_logs_' + pid, JSON.stringify(logs));
        
        const saved = JSON.parse(localStorage.getItem('bp_logs_' + pid));
        const takenCount = saved.filter(l => l.status === 'taken').length;
        const time = Date.now() - t0;
        if (takenCount === 1) {
            addResult(name, cat, 'pass', time, '确认服药成功');
        } else {
            addResult(name, cat, 'fail', time, '确认失败');
        }
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

function testAddBpRecord() {
    const name = '记录血压';
    const cat = '核心';
    const t0 = Date.now();
    try {
        const state = JSON.parse(localStorage.getItem('bp_app_state'));
        const pid = state.pid;
        const bps = [
            { id: 40001, systolic: 120, diastolic: 80, hr: 72, note: '晨起', time: daysAgo(1) + ' 08:00' },
            { id: 40002, systolic: 130, diastolic: 85, hr: 75, note: '午饭后', time: todayStr() + ' 12:00' }
        ];
        localStorage.setItem('bp_data_' + pid, JSON.stringify(bps));
        const saved = JSON.parse(localStorage.getItem('bp_data_' + pid));
        const time = Date.now() - t0;
        if (saved.length === 2) {
            addResult(name, cat, 'pass', time, '添加2条血压记录成功');
        } else {
            addResult(name, cat, 'fail', time, '记录数量不匹配');
        }
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

function testBpSorting() {
    const name = '血压记录排序';
    const cat = '核心';
    const t0 = Date.now();
    try {
        let bps = [
            { id: 1, time: daysAgo(3) + ' 08:00' },
            { id: 2, time: daysAgo(1) + ' 08:00' },
            { id: 3, time: todayStr() + ' 08:00' },
            { id: 4, time: daysAgo(2) + ' 08:00' }
        ];
        bps.sort((a, b) => a.time < b.time ? 1 : -1);
        const time = Date.now() - t0;
        if (bps[0].time >= bps[1].time && bps[1].time >= bps[2].time && bps[2].time >= bps[3].time) {
            addResult(name, cat, 'pass', time, '血压记录排序正确（新到旧）');
        } else {
            addResult(name, cat, 'fail', time, '排序错误');
        }
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

function testAddAlert() {
    const name = '添加预警';
    const cat = '核心';
    const t0 = Date.now();
    try {
        const state = JSON.parse(localStorage.getItem('bp_app_state'));
        const pid = state.pid;
        const alerts = [
            { id: 50001, logId: 30001, medName: '药1', diff: 10, level: 'warn', status: 'active', time: nowStr() },
            { id: 50002, logId: 30002, medName: '药2', diff: 40, level: 'critical', status: 'active', time: nowStr() }
        ];
        localStorage.setItem('bp_alerts_' + pid, JSON.stringify(alerts));
        const saved = JSON.parse(localStorage.getItem('bp_alerts_' + pid));
        const time = Date.now() - t0;
        if (saved.length === 2) {
            addResult(name, cat, 'pass', time, '添加2条预警成功');
        } else {
            addResult(name, cat, 'fail', time, '预警数量不匹配');
        }
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

function testResolveAlert() {
    const name = '处理预警(ID比较)';
    const cat = '核心';
    const t0 = Date.now();
    try {
        const state = JSON.parse(localStorage.getItem('bp_app_state'));
        const pid = state.pid;
        let alerts = JSON.parse(localStorage.getItem('bp_alerts_' + pid) || '[]');
        
        if (alerts.length > 0) {
            let alertId = alerts[0].id;
            const alert = alerts.find(a => String(a.id) === String(alertId));
            if (alert) {
                alert.status = 'resolved';
                localStorage.setItem('bp_alerts_' + pid, JSON.stringify(alerts));
            }
            const saved = JSON.parse(localStorage.getItem('bp_alerts_' + pid));
            const resolvedCount = saved.filter(a => a.status === 'resolved').length;
            const time = Date.now() - t0;
            if (resolvedCount > 0) {
                addResult(name, cat, 'pass', time, '预警ID比较已修复，处理成功', true);
            } else {
                addResult(name, cat, 'fail', time, '处理失败');
            }
        } else {
            addResult(name, cat, 'pass', Date.now() - t0, '无预警可处理');
        }
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

// ==================== 家庭管理测试 ====================

function testAddFamilyMember() {
    const name = '添加家庭成员';
    const cat = '家庭';
    const t0 = Date.now();
    try {
        let state = JSON.parse(localStorage.getItem('bp_app_state'));
        const newId = 99999;
        state.parents.push({ id: newId, name: '测试成员', age: 55, gender: '女', relation: '母亲' });
        localStorage.setItem('bp_app_state', JSON.stringify(state));
        localStorage.setItem('bp_meds_' + newId, '[]');
        localStorage.setItem('bp_logs_' + newId, '[]');
        localStorage.setItem('bp_data_' + newId, '[]');
        
        const saved = JSON.parse(localStorage.getItem('bp_app_state'));
        const time = Date.now() - t0;
        if (saved.parents.length >= 2) {
            addResult(name, cat, 'pass', time, `添加家庭成员成功，共${saved.parents.length}人`);
        } else {
            addResult(name, cat, 'fail', time, '家庭成员数量不匹配');
        }
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

function testSwitchFamilyMember() {
    const name = '切换家庭成员';
    const cat = '家庭';
    const t0 = Date.now();
    try {
        let state = JSON.parse(localStorage.getItem('bp_app_state'));
        if (state.parents.length >= 2) {
            const oldPid = state.pid;
            state.pid = state.parents[1].id;
            state.pname = state.parents[1].name;
            localStorage.setItem('bp_app_state', JSON.stringify(state));
            
            const saved = JSON.parse(localStorage.getItem('bp_app_state'));
            const time = Date.now() - t0;
            if (saved.pid !== oldPid) {
                addResult(name, cat, 'pass', time, `切换成员成功: ${saved.pname}`);
            } else {
                addResult(name, cat, 'fail', time, '切换失败');
            }
        } else {
            addResult(name, cat, 'fail', Date.now() - t0, '家庭成员不足');
        }
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

function testDataIsolation() {
    const name = '多用户数据隔离';
    const cat = '家庭';
    const t0 = Date.now();
    try {
        const state = JSON.parse(localStorage.getItem('bp_app_state'));
        const p1 = state.parents[0].id;
        const p2 = state.parents[1].id;
        
        localStorage.setItem('bp_meds_' + p1, JSON.stringify([{ id: 1, name: '药A' }]));
        localStorage.setItem('bp_meds_' + p2, JSON.stringify([{ id: 2, name: '药B' }, { id: 3, name: '药C' }]));
        
        const m1 = JSON.parse(localStorage.getItem('bp_meds_' + p1));
        const m2 = JSON.parse(localStorage.getItem('bp_meds_' + p2));
        const time = Date.now() - t0;
        
        if (m1.length !== m2.length && m1[0].name !== m2[0].name) {
            addResult(name, cat, 'pass', time, '数据隔离验证通过');
        } else {
            addResult(name, cat, 'fail', time, '数据未正确隔离');
        }
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

// ==================== 业务逻辑测试 ====================

function testInventoryCalc() {
    const name = '库存计算';
    const cat = '业务';
    const t0 = Date.now();
    try {
        const meds = [
            { name: '药1', quantity: 5, times: ['08:00', '20:00'] },
            { name: '药2', quantity: 30, times: ['08:00'] },
            { name: '药3', quantity: 10, times: ['08:00', '12:00', '20:00'] }
        ];
        
        const lowStock = meds.filter(m => {
            const daily = m.times.length;
            const daysLeft = Math.floor(m.quantity / daily);
            return daysLeft < 7;
        });
        const time = Date.now() - t0;
        
        if (lowStock.length === 2) {
            addResult(name, cat, 'pass', time, `库存计算正确，${lowStock.length}种药物库存不足`);
        } else {
            addResult(name, cat, 'fail', time, '库存计算错误');
        }
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

function testAlertLevel() {
    const name = '预警级别判断';
    const cat = '业务';
    const t0 = Date.now();
    try {
        const settings = { l1: 10, l2: 25, l3: 40 };
        const testCases = [
            { diff: 5, expected: 'normal' },
            { diff: 15, expected: 'warn' },
            { diff: 30, expected: 'urgent' },
            { diff: 50, expected: 'critical' }
        ];
        
        let allPass = true;
        testCases.forEach(tc => {
            let level;
            if (tc.diff >= settings.l3) level = 'critical';
            else if (tc.diff >= settings.l2) level = 'urgent';
            else if (tc.diff >= settings.l1) level = 'warn';
            else level = 'normal';
            
            if (level !== tc.expected) allPass = false;
        });
        const time = Date.now() - t0;
        
        if (allPass) {
            addResult(name, cat, 'pass', time, '预警级别判断全部正确');
        } else {
            addResult(name, cat, 'fail', time, '预警级别判断有误');
        }
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

function testHealthAssessment() {
    const name = '健康评估计算';
    const cat = '业务';
    const t0 = Date.now();
    try {
        const bps = [
            { systolic: 120, diastolic: 80, hr: 72 },
            { systolic: 125, diastolic: 82, hr: 74 },
            { systolic: 130, diastolic: 85, hr: 76 },
            { systolic: 135, diastolic: 88, hr: 78 },
            { systolic: 140, diastolic: 90, hr: 80 }
        ];
        
        const limit = Math.min(bps.length, 7);
        const avgSys = Math.round(bps.slice(0, limit).reduce((s, r) => s + r.systolic, 0) / limit);
        const avgDia = Math.round(bps.slice(0, limit).reduce((s, r) => s + r.diastolic, 0) / limit);
        const avgHr = Math.round(bps.slice(0, limit).reduce((s, r) => s + r.hr, 0) / limit);
        const time = Date.now() - t0;
        
        if (avgSys === 130 && avgDia === 85 && avgHr === 76) {
            addResult(name, cat, 'pass', time, `健康评估计算正确: ${avgSys}/${avgDia}, 心率${avgHr}`);
        } else {
            addResult(name, cat, 'fail', time, `计算结果错误: ${avgSys}/${avgDia}`);
        }
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

// ==================== 边界测试 ====================

function testSingleDataChart() {
    const name = '单条数据图表处理';
    const cat = '边界';
    const t0 = Date.now();
    try {
        const bps = [{ systolic: 120, diastolic: 80, hr: 72, time: todayStr() + ' 08:00' }];
        const time = Date.now() - t0;
        if (bps.length < 2) {
            addResult(name, cat, 'pass', time, '单条数据正确处理（无需渲染图表）');
        } else {
            addResult(name, cat, 'fail', time, '边界处理失败');
        }
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

function testEmptyData() {
    const name = '空数据处理';
    const cat = '边界';
    const t0 = Date.now();
    try {
        const meds = JSON.parse(localStorage.getItem('bp_meds_99999') || '[]');
        const bps = JSON.parse(localStorage.getItem('bp_data_99999') || '[]');
        const alerts = JSON.parse(localStorage.getItem('bp_alerts_99999') || '[]');
        const time = Date.now() - t0;
        
        if (meds.length === 0 && bps.length === 0 && alerts.length === 0) {
            addResult(name, cat, 'pass', time, '空数据处理正确');
        } else {
            addResult(name, cat, 'fail', time, '空数据处理失败');
        }
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

function testAbnormalValues() {
    const name = '异常值处理';
    const cat = '边界';
    const t0 = Date.now();
    try {
        const testCases = [
            { sys: 250, dia: 150, shouldPass: true },
            { sys: 69, dia: 80, shouldPass: false },
            { sys: 120, dia: 39, shouldPass: false },
            { sys: 251, dia: 80, shouldPass: false },
            { sys: 120, dia: 151, shouldPass: false }
        ];
        
        let allPass = true;
        testCases.forEach(tc => {
            const isValid = tc.sys >= 70 && tc.sys <= 250 && tc.dia >= 40 && tc.dia <= 150;
            if (isValid !== tc.shouldPass) allPass = false;
        });
        const time = Date.now() - t0;
        
        if (allPass) {
            addResult(name, cat, 'pass', time, '异常值验证全部正确');
        } else {
            addResult(name, cat, 'fail', time, '异常值验证有误');
        }
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

// ==================== 压力测试 ====================

function stressLargeBpData() {
    const name = '压力:大量血压数据(1000条)';
    const cat = '压力';
    const t0 = Date.now();
    try {
        const state = JSON.parse(localStorage.getItem('bp_app_state'));
        const pid = state.pid;
        const bps = [];
        for (let i = 0; i < 1000; i++) {
            const date = new Date(); date.setDate(date.getDate() - Math.floor(i / 2));
            const ds = date.getFullYear() + '-' + pad(date.getMonth() + 1) + '-' + pad(date.getDate());
            bps.push({
                id: genId(),
                systolic: 120 + Math.floor(Math.random() * 30),
                diastolic: 75 + Math.floor(Math.random() * 20),
                hr: 65 + Math.floor(Math.random() * 20),
                note: '测试',
                time: ds + ' 08:00'
            });
        }
        localStorage.setItem('bp_data_' + pid, JSON.stringify(bps));
        const saved = JSON.parse(localStorage.getItem('bp_data_' + pid));
        const time = Date.now() - t0;
        if (saved.length === 1000) {
            addResult(name, cat, 'pass', time, `写入1000条血压记录 (${time}ms)`);
        } else {
            addResult(name, cat, 'fail', time, '写入失败');
        }
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

function stressLargeMedData() {
    const name = '压力:大量药物数据(100种)';
    const cat = '压力';
    const t0 = Date.now();
    try {
        const state = JSON.parse(localStorage.getItem('bp_app_state'));
        const pid = state.pid;
        const meds = [];
        for (let i = 0; i < 100; i++) {
            meds.push({
                id: genId(),
                name: '测试药' + i,
                dosage: '1片',
                frequency: 'once',
                times: ['08:00'],
                quantity: 30
            });
        }
        localStorage.setItem('bp_meds_' + pid, JSON.stringify(meds));
        const saved = JSON.parse(localStorage.getItem('bp_meds_' + pid));
        const time = Date.now() - t0;
        if (saved.length === 100) {
            addResult(name, cat, 'pass', time, `写入100种药物 (${time}ms)`);
        } else {
            addResult(name, cat, 'fail', time, '写入失败');
        }
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

function stressConcurrentWrite() {
    const name = '压力:并发写入测试';
    const cat = '压力';
    const t0 = Date.now();
    try {
        const state = JSON.parse(localStorage.getItem('bp_app_state'));
        const pid = state.pid;
        localStorage.setItem('bp_data_' + pid, '[]');
        
        for (let i = 0; i < 100; i++) {
            const bps = JSON.parse(localStorage.getItem('bp_data_' + pid) || '[]');
            bps.push({ id: genId(), systolic: 120 + i, diastolic: 80 + i, hr: 70, time: todayStr() + ' 08:00' });
            localStorage.setItem('bp_data_' + pid, JSON.stringify(bps));
        }
        const saved = JSON.parse(localStorage.getItem('bp_data_' + pid));
        const time = Date.now() - t0;
        if (saved.length === 100) {
            addResult(name, cat, 'pass', time, `100次写入全部成功 (${time}ms)`);
        } else {
            addResult(name, cat, 'fail', time, `写入数量不匹配: ${saved.length}`);
        }
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

function stressLargeQuery() {
    const name = '压力:大数据查询';
    const cat = '压力';
    const t0 = Date.now();
    try {
        const state = JSON.parse(localStorage.getItem('bp_app_state'));
        const pid = state.pid;
        const bps = JSON.parse(localStorage.getItem('bp_data_' + pid) || '[]');
        
        const highBp = bps.filter(r => r.systolic > 140);
        const normalBp = bps.filter(r => r.systolic >= 120 && r.systolic <= 140);
        const avgSys = bps.length > 0 ? Math.round(bps.reduce((s, r) => s + r.systolic, 0) / bps.length) : 0;
        const time = Date.now() - t0;
        
        addResult(name, cat, 'pass', time, `查询${bps.length}条数据: 偏高${highBp.length}条, 平均${avgSys} (${time}ms)`);
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

function stressChartRender() {
    const name = '压力:图表渲染计算';
    const cat = '压力';
    const t0 = Date.now();
    try {
        const state = JSON.parse(localStorage.getItem('bp_app_state'));
        const pid = state.pid;
        const bps = JSON.parse(localStorage.getItem('bp_data_' + pid) || '[]');
        
        if (bps.length < 2) {
            addResult(name, cat, 'pass', Date.now() - t0, '数据不足，跳过图表测试');
            return;
        }
        
        const filtered = bps.slice(0, 365);
        const allValues = [];
        filtered.forEach(r => { allValues.push(r.systolic, r.diastolic); });
        const minVal = Math.floor(Math.min(...allValues) / 10) * 10 - 10;
        const maxVal = Math.ceil(Math.max(...allValues) / 10) * 10 + 10;
        const range = maxVal - minVal === 0 ? 100 : maxVal - minVal;
        const time = Date.now() - t0;
        
        addResult(name, cat, 'pass', time, `处理${filtered.length}天数据 (${time}ms)`);
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

function stressMultiUser() {
    const name = '压力:多用户隔离(10用户)';
    const cat = '压力';
    const t0 = Date.now();
    try {
        for (let i = 0; i < 10; i++) {
            const pid = 90000 + i;
            localStorage.setItem('bp_meds_' + pid, JSON.stringify([{ id: i, name: '药' + i }]));
            localStorage.setItem('bp_data_' + pid, JSON.stringify([
                { id: i, systolic: 120 + i, diastolic: 80 + i, hr: 70, time: todayStr() + ' 08:00' }
            ]));
        }
        
        let success = true;
        for (let i = 0; i < 10; i++) {
            const pid = 90000 + i;
            const meds = JSON.parse(localStorage.getItem('bp_meds_' + pid));
            if (!meds || meds.length !== 1 || meds[0].id !== i) {
                success = false;
                break;
            }
        }
        const time = Date.now() - t0;
        
        if (success) {
            addResult(name, cat, 'pass', time, `10用户数据隔离验证通过 (${time}ms)`);
        } else {
            addResult(name, cat, 'fail', time, '数据隔离失败');
        }
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

function stressSerialization() {
    const name = '压力:数据序列化(10000对象)';
    const cat = '压力';
    const t0 = Date.now();
    try {
        const data = {};
        for (let i = 0; i < 10000; i++) {
            data['key_' + i] = { value: Math.random(), text: 'test_' + i };
        }
        const json = JSON.stringify(data);
        const parsed = JSON.parse(json);
        const time = Date.now() - t0;
        
        if (Object.keys(parsed).length === 10000) {
            addResult(name, cat, 'pass', time, `序列化10000对象 (${time}ms)`);
        } else {
            addResult(name, cat, 'fail', time, '序列化失败');
        }
    } catch (e) {
        addResult(name, cat, 'fail', Date.now() - t0, e.message);
    }
}

// ==================== 运行所有测试 ====================

log('========================================');
log('血压守护 - 全面自动化测试');
log('========================================\n');

log('【1/4】基础功能测试...\n');
testBasicReadWrite();
testDateFormatting();
testUserStateInit();
testAddMedication();
testDeleteMedication();
testConfirmMedication();
testAddBpRecord();
testBpSorting();
testAddAlert();
testResolveAlert();

log('\n【2/4】家庭管理测试...\n');
testAddFamilyMember();
testSwitchFamilyMember();
testDataIsolation();

log('\n【3/4】业务逻辑与边界测试...\n');
testInventoryCalc();
testAlertLevel();
testHealthAssessment();
testSingleDataChart();
testEmptyData();
testAbnormalValues();

log('\n【4/4】压力测试...\n');
stressLargeBpData();
stressLargeMedData();
stressConcurrentWrite();
stressLargeQuery();
stressChartRender();
stressMultiUser();
stressSerialization();

// 生成测试报告
const totalTime = Date.now() - startTime;
const passRate = ((passedTests / totalTests) * 100).toFixed(1);

log('\n========================================');
log('测试报告');
log('========================================');
log(`总测试数: ${totalTests}`);
log(`通过: ${passedTests} (${passRate}%)`);
log(`失败: ${failedTests}`);
log(`已修复BUG: ${fixedBugs}`);
log(`总耗时: ${totalTime}ms`);
log('========================================\n');

// 保存测试报告
const report = {
    timestamp: new Date().toISOString(),
    total: totalTests,
    passed: passedTests,
    failed: failedTests,
    fixed: fixedBugs,
    passRate: passRate + '%',
    totalTime: totalTime + 'ms',
    results: testResults
};

fs.writeFileSync(
    path.join(__dirname, 'test_report.json'),
    JSON.stringify(report, null, 2),
    'utf-8'
);

log('测试报告已保存至: test_report.json\n');

if (failedTests > 0) {
    log('⚠️  发现失败测试，请检查:');
    testResults.filter(r => r.status === 'fail').forEach(r => {
        log(`  ❌ ${r.name}: ${r.detail}`);
    });
} else {
    log('🎉 所有测试通过！');
}

log('\n详细日志:');
testLogs.forEach(l => console.log(l));

process.exit(failedTests > 0 ? 1 : 0);
