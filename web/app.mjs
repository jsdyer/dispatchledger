import { el, fmt, put, setOptions, start, table } from './ui.mjs';
import { difference } from './model.mjs';
start(data => {
  const labels = {'Combined':'Combined','HRP':'Halifax Regional Police','RCMP':'RCMP Halifax Regional Detachment'};
  setOptions('first', Object.values(labels), 'Combined');
  setOptions('second', Object.keys(data.calls.Combined), 'Public-generated calls');
  function render() {
    const key = Object.keys(labels).find(k => labels[k] === el('first').value);
    const measure = el('second').value, pair = data.calls[key][measure];
    const delta = difference(pair);
    put('label1','January–June 2024'); put('value1',fmt(pair[0]));
    put('label2','January–June 2025'); put('value2',fmt(pair[1]));
    put('finding', measure + ' ' + (delta.number < 0 ? 'fell' : 'rose') + ' by ' + fmt(Math.abs(delta.number)) +
        ' (' + Math.abs(delta.percent).toFixed(1) + '%) for ' + labels[key] + '.');
    table('history',['Measure','Jan–Jun 2024','Jan–Jun 2025'],Object.entries(data.calls[key]).map(([name,values])=>[name,...values.map(fmt)]));
    const rows = Object.entries(data.districts).filter(([agency])=>key === 'Combined' || agency === key)
      .flatMap(([agency,districts]) => Object.entries(districts).map(([district,n])=>[district + ' · ' + agency,...n.map(fmt)]));
    table('districts',['Division','Person','Property','Other Criminal Code','Total'],rows);
  }
  el('explore').addEventListener('change',render); render();
});
