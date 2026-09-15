import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, '..');
const source = readFileSync(resolve(root, 'src', 'site.js'), 'utf8');
const projects = JSON.parse(readFileSync(resolve(root, 'data', 'projects.json'), 'utf8'));

class ClassList {
  constructor(...tokens) { this.tokens = new Set(tokens); }
  add(token) { this.tokens.add(token); }
  remove(token) { this.tokens.delete(token); }
  toggle(token, force) {
    const enabled = force === undefined ? !this.tokens.has(token) : Boolean(force);
    enabled ? this.tokens.add(token) : this.tokens.delete(token);
    return enabled;
  }
  contains(token) { return this.tokens.has(token); }
}

let document;
class Element {
  constructor({ dataset = {}, textContent = '', value = '', hidden = false } = {}) {
    this.dataset = { ...dataset };
    this.textContent = textContent;
    this.value = value;
    this.hidden = hidden;
    this.classList = new ClassList();
    this.listeners = new Map();
    this.attributes = new Map();
    this.childrenBySelector = new Map();
  }
  addEventListener(type, handler) {
    const handlers = this.listeners.get(type) || [];
    handlers.push(handler);
    this.listeners.set(type, handlers);
  }
  async emit(type) {
    const event = { target: this, preventDefault() {} };
    for (const handler of this.listeners.get(type) || []) await handler(event);
  }
  setAttribute(name, value) { this.attributes.set(name, String(value)); }
  getAttribute(name) { return this.attributes.get(name) ?? null; }
  querySelector(selector) { return this.childrenBySelector.get(selector) ?? null; }
  focus() { document.activeElement = this; }
  select() { this.selected = true; }
}

const rows = [...projects].sort((a, b) => b.id - a.id).map(project => new Element({
  dataset: {
    ledgerId: String(project.id),
    ledgerCategory: project.category,
    ledgerStatus: project.status,
    ledgerSearch: `${project.name} ${project.subtitle} ${new URL(project.url).hostname}`.toLowerCase(),
  },
}));
const filters = ['all', 'ai', 'game', 'tool', 'creative'].map((value, index) => {
  const element = new Element({ dataset: { ledgerFilter: value } });
  element.setAttribute('aria-pressed', index === 0 ? 'true' : 'false');
  return element;
});
const search = new Element();
const status = new Element({ value: 'all' });
const count = new Element({ textContent: '43 / 43' });
const empty = new Element({ hidden: true });
const tools = new Element({ hidden: true });
const more = new Element({ textContent: '查看全部 43 条记录', hidden: true });
more.setAttribute('aria-expanded', 'false');
const copyButton = new Element({ dataset: { copyValue: 'wang1227928718' }, textContent: '复制微信号', hidden: true });
const copyStatus = new Element();
const manual = new Element({ hidden: true });
const manualInput = new Element({ value: 'wang1227928718' });
manual.childrenBySelector.set('input', manualInput);
const html = new Element();
const viewSwitch = new Element({ hidden: true });
const wall = new Element();
const viewButtons = ['wall', 'list'].map(view => new Element({ dataset: { view } }));

const one = new Map([
  ['.view-switch', viewSwitch],
  ['#ledger-list', wall],
  ['#ledger-search', search],
  ['.ledger-tools', tools],
  ['#ledger-status', status],
  ['#ledger-count', count],
  ['#ledger-empty', empty],
  ['#ledger-more', more],
  ['[data-copy-value]', copyButton],
  ['#copy-status', copyStatus],
  ['.manual-copy', manual],
]);
document = {
  activeElement: null,
  documentElement: html,
  querySelector: selector => one.get(selector) ?? null,
  querySelectorAll: selector => {
    if (selector === '[data-view]') return viewButtons;
    if (selector === '[data-ledger-id]') return rows;
    if (selector === '[data-ledger-filter]') return filters;
    return [];
  },
  execCommand: () => true,
};
const navigator = { clipboard: { writeText: async () => {} } };

new Function('document', 'navigator', source)(document, navigator);

const visibleRows = () => rows.filter(row => !row.hidden);
assert.equal(tools.hidden, false);
assert.equal(copyButton.hidden, false);
assert.equal(visibleRows().length, 9, 'default ledger matches the V11 compact specification');
assert.equal(count.textContent, '43 / 43');
assert.equal(more.hidden, false);

await filters.find(filter => filter.dataset.ledgerFilter === 'ai').emit('click');
assert.equal(visibleRows().length, 5);
assert.equal(count.textContent, '5 / 43');
assert.equal(more.hidden, true);
assert.ok(visibleRows().every(row => row.dataset.ledgerCategory === 'ai'));

await filters.find(filter => filter.dataset.ledgerFilter === 'game').emit('click');
assert.equal(visibleRows().length, 20);
assert.equal(count.textContent, '20 / 43');
assert.ok(visibleRows().every(row => row.dataset.ledgerCategory === 'game'));

await filters[0].emit('click');
status.value = 'offline';
await status.emit('change');
assert.equal(visibleRows().length, 1);
assert.equal(visibleRows()[0].dataset.ledgerId, '24');
assert.equal(count.textContent, '1 / 43');

status.value = 'all';
await status.emit('change');
search.value = 'astra';
await search.emit('input');
assert.equal(visibleRows().length, 1);
assert.equal(visibleRows()[0].dataset.ledgerId, '37');
assert.equal(visibleRows()[0].dataset.ledgerCategory, 'ai');
assert.equal(empty.hidden, true);

search.value = 'narinig';
await search.emit('input');
assert.equal(visibleRows().length, 1);
assert.equal(visibleRows()[0].dataset.ledgerId, '38');
assert.equal(visibleRows()[0].dataset.ledgerCategory, 'game');
assert.equal(empty.hidden, true);

search.value = 'halloween';
await search.emit('input');
assert.equal(visibleRows().length, 1);
assert.equal(visibleRows()[0].dataset.ledgerId, '39');
assert.equal(visibleRows()[0].dataset.ledgerCategory, 'game');
assert.equal(empty.hidden, true);

search.value = 'mimicparty';
await search.emit('input');
assert.equal(visibleRows().length, 1);
assert.equal(visibleRows()[0].dataset.ledgerId, '40');
assert.equal(visibleRows()[0].dataset.ledgerCategory, 'game');
assert.equal(empty.hidden, true);

search.value = 'parrygrid';
await search.emit('input');
assert.equal(visibleRows().length, 1);
assert.equal(visibleRows()[0].dataset.ledgerId, '41');
assert.equal(visibleRows()[0].dataset.ledgerCategory, 'game');
assert.equal(empty.hidden, true);

search.value = 'commandanarmy';
await search.emit('input');
assert.equal(visibleRows().length, 1);
assert.equal(visibleRows()[0].dataset.ledgerId, '43');
assert.equal(visibleRows()[0].dataset.ledgerCategory, 'game');

search.value = '1666amsterdam';
await search.emit('input');
assert.equal(visibleRows().length, 1);
assert.equal(visibleRows()[0].dataset.ledgerId, '42');
assert.equal(visibleRows()[0].dataset.ledgerCategory, 'game');
assert.equal(empty.hidden, true);

// Switching presentation keeps the active search and result intact.
assert.equal(viewSwitch.hidden, false);
await viewButtons[1].emit('click');
assert.equal(wall.classList.contains('is-list'), true);
assert.equal(viewButtons[1].getAttribute('aria-pressed'), 'true');
assert.equal(viewButtons[0].getAttribute('aria-pressed'), 'false');
assert.equal(search.value, '1666amsterdam');
assert.equal(visibleRows().length, 1);
await viewButtons[0].emit('click');
assert.equal(wall.classList.contains('is-list'), false);
assert.equal(viewButtons[0].getAttribute('aria-pressed'), 'true');
assert.equal(visibleRows()[0].dataset.ledgerId, '42');

search.value = 'onimusha';
await search.emit('input');
assert.equal(visibleRows().length, 1);
assert.equal(visibleRows()[0].dataset.ledgerId, '36');
assert.equal(visibleRows()[0].dataset.ledgerCategory, 'game');
assert.equal(empty.hidden, true);

search.value = 'dawnwalker';
await search.emit('input');
assert.equal(visibleRows().length, 1);
assert.equal(visibleRows()[0].dataset.ledgerId, '35');
assert.equal(visibleRows()[0].dataset.ledgerCategory, 'game');
assert.equal(empty.hidden, true);

search.value = 'definitely-not-a-project';
await search.emit('input');
assert.equal(visibleRows().length, 0);
assert.equal(count.textContent, '0 / 43');
assert.equal(empty.hidden, false);

search.value = '';
await search.emit('input');
assert.equal(empty.hidden, true);
await more.emit('click');
assert.equal(visibleRows().length, 43);
assert.equal(more.getAttribute('aria-expanded'), 'true');
assert.equal(more.textContent, '收起发布档案');

await copyButton.emit('click');
assert.equal(copyStatus.textContent, '微信号已复制，可以直接添加。');
assert.equal(copyButton.textContent, '已复制 ✓');
assert.equal(manual.hidden, true);

navigator.clipboard.writeText = async () => { throw new Error('denied'); };
document.execCommand = () => false;
copyButton.textContent = '复制微信号';
copyStatus.textContent = '';
await copyButton.emit('click');
assert.equal(copyButton.textContent, '复制微信号');
assert.equal(copyStatus.textContent, '复制失败，请在下方手动复制微信号。');
assert.equal(manual.hidden, false);
assert.equal(manualInput.selected, true);
assert.equal(document.activeElement, manualInput);

assert.equal(source.includes('requestAnimationFrame'), false);
console.log('v11 interactions: OK (ledger combination, empty state, expansion, copy success/fallback)');
