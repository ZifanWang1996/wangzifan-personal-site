import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const html = readFileSync(resolve(here, '..', 'index.html'), 'utf8');
const scriptMatch = html.match(/<script>\s*([\s\S]*?)<\/script>/);
assert.ok(scriptMatch, 'inline script not found');

class ClassList {
  constructor(...tokens) { this.tokens = new Set(tokens.filter(Boolean)); }
  add(token) { this.tokens.add(token); }
  remove(token) { this.tokens.delete(token); }
  contains(token) { return this.tokens.has(token); }
  toggle(token, force) {
    const enabled = force === undefined ? !this.tokens.has(token) : Boolean(force);
    enabled ? this.tokens.add(token) : this.tokens.delete(token);
    return enabled;
  }
}

let document;
class Element {
  constructor(name, { dataset = {}, textContent = '', hidden = false, classes = [], focusable = true } = {}) {
    this.name = name;
    this.dataset = { ...dataset };
    this.textContent = textContent;
    this.hidden = hidden;
    this.focusable = focusable;
    this.isConnected = true;
    this.classList = new ClassList(...classes);
    this.attributes = new Map();
    this.listeners = new Map();
    this.style = {};
    this.parentNode = null;
    this.one = new Map();
    this.many = new Map();
  }
  addEventListener(type, handler) {
    const handlers = this.listeners.get(type) || [];
    handlers.push(handler);
    this.listeners.set(type, handlers);
  }
  async emit(type, init = {}) {
    const event = makeEvent({ target: this, ...init });
    for (const handler of this.listeners.get(type) || []) await handler(event);
    return event;
  }
  setAttribute(name, value) { this.attributes.set(name, String(value)); }
  getAttribute(name) { return this.attributes.get(name) ?? null; }
  focus() { if (this.focusable && this.isConnected) document.activeElement = this; }
  contains(element) {
    for (let current = element; current; current = current.parentNode) if (current === this) return true;
    return false;
  }
  closest(selector) {
    if (selector !== '[hidden]') return null;
    for (let current = this; current; current = current.parentNode) if (current.hidden) return current;
    return null;
  }
  querySelector(selector) { return this.one.get(selector) ?? null; }
  querySelectorAll(selector) { return this.many.get(selector) ?? []; }
  select() { this.selected = true; }
  remove() {
    if (!this.parentNode) return;
    const at = this.parentNode.children.indexOf(this);
    if (at >= 0) this.parentNode.children.splice(at, 1);
    this.parentNode = null;
    this.isConnected = false;
  }
}

function makeEvent(init = {}) {
  return {
    key: '', ctrlKey: false, metaKey: false, shiftKey: false,
    clientX: 0, clientY: 0, defaultPrevented: false,
    preventDefault() { this.defaultPrevented = true; },
    ...init,
  };
}

const rootStyle = new Map();
const rootElement = new Element('html', { focusable: false });
rootElement.style = { setProperty: (name, value) => rootStyle.set(name, value) };
const body = new Element('body', { focusable: false });
body.parentNode = rootElement;
body.children = [];
body.appendChild = element => { element.parentNode = body; element.isConnected = true; body.children.push(element); return element; };

const filterSpecs = [
  ['all', '全部'], ['ai', 'AI 产品'], ['game', '游戏与内容'],
  ['tool', '实用工具'], ['creative', '创意实验'],
];
const filters = filterSpecs.map(([value, label], index) => {
  const element = new Element(`filter-${value}`, { dataset: { filter: value }, textContent: label, classes: index === 0 ? ['active'] : [] });
  element.setAttribute('aria-pressed', index === 0 ? 'true' : 'false');
  return element;
});
const categories = [...Array(3).fill('ai'), ...Array(9).fill('game'), ...Array(9).fill('tool'), ...Array(5).fill('creative')];
const projects = categories.map((category, index) => {
  const card = new Element(`project-${index + 1}`, { classes: ['site'] });
  card.one.set('[data-category]', new Element(`category-${index + 1}`, { dataset: { category } }));
  return card;
});

const visibleCount = new Element('visibleCount', { textContent: 'ALL RELEASES' });
const modal = new Element('commandDialog', { hidden: true, classes: ['modal'] });
const openButton = new Element('commandBtn');
openButton.setAttribute('aria-expanded', 'false');
const closeButton = new Element('commandClose');
const modalLinks = Array.from({ length: 4 }, (_, index) => new Element(`command-link-${index + 1}`));
modal.parentNode = body;
openButton.parentNode = body;
closeButton.parentNode = modal;
for (const link of modalLinks) link.parentNode = modal;
modal.one.set('a', modalLinks[0]);
modal.many.set('a', modalLinks);
modal.many.set('a,button:not([disabled])', [closeButton, ...modalLinks]);
const copyButton = new Element('copyWechat', { dataset: { copy: 'wang1227928718' }, textContent: '复制微信号' });
const copyStatus = new Element('copyStatus');
const year = new Element('year');

const allSelectors = new Map([
  ['#visibleCount', visibleCount], ['#commandDialog', modal], ['#commandBtn', openButton],
  ['#commandClose', closeButton], ['#copyWechat', copyButton], ['#copyStatus', copyStatus], ['#year', year],
]);
document = {
  activeElement: body,
  body,
  documentElement: rootElement,
  querySelector: selector => allSelectors.get(selector) ?? null,
  querySelectorAll: selector => selector === '.filter' ? filters : selector === '.site' ? projects : [],
  createElement: tag => new Element(tag),
  execCommand: () => true,
};

const windowListeners = new Map();
function addEventListener(type, handler) {
  const handlers = windowListeners.get(type) || [];
  handlers.push(handler);
  windowListeners.set(type, handlers);
}
async function dispatchWindow(type, init = {}) {
  const event = makeEvent(init);
  for (const handler of windowListeners.get(type) || []) await handler(event);
  return event;
}
const navigator = { clipboard: { writeText: async () => {} } };
const matchMedia = () => ({ matches: false });
const requestAnimationFrame = callback => { callback(); return 1; };

new Function('document', 'navigator', 'matchMedia', 'addEventListener', 'requestAnimationFrame', scriptMatch[1])(
  document, navigator, matchMedia, addEventListener, requestAnimationFrame,
);

for (const [value, expected] of [['ai', 3], ['game', 9], ['tool', 9], ['creative', 5], ['all', 26]]) {
  const button = filters.find(item => item.dataset.filter === value);
  await button.emit('click');
  assert.equal(projects.filter(card => !card.classList.contains('hide')).length, expected, `${value} visible count`);
  for (const item of filters) assert.equal(item.getAttribute('aria-pressed'), String(item === button), `${value} aria state`);
  assert.equal(visibleCount.textContent, value === 'all' ? 'ALL RELEASES' : button.textContent.toUpperCase());
}

assert.equal(document.activeElement, body);
let event = await dispatchWindow('keydown', { key: 'k', ctrlKey: true });
assert.equal(event.defaultPrevented, true);
assert.equal(modal.hidden, false);
assert.equal(document.activeElement, modalLinks[0]);
await dispatchWindow('keydown', { key: 'Escape' });
assert.equal(modal.hidden, true);
assert.equal(document.activeElement, openButton, 'BODY shortcut path must fall back to command button');
assert.equal(modal.contains(document.activeElement), false, 'focus must not remain in hidden dialog');
assert.equal(document.activeElement.closest('[hidden]'), null);

const origin = new Element('origin');
origin.parentNode = body;
origin.focus();
event = await dispatchWindow('keydown', { key: 'k', ctrlKey: true });
assert.equal(event.defaultPrevented, true);
assert.equal(modal.hidden, false);
assert.equal(document.activeElement, modalLinks[0]);
await dispatchWindow('keydown', { key: 'Escape' });
assert.equal(modal.hidden, true);
assert.equal(document.activeElement, origin, 'focusable shortcut origin must be restored');
assert.equal(modal.contains(document.activeElement), false);

openButton.focus();
await openButton.emit('click');
assert.equal(modal.hidden, false);
assert.equal(modal.classList.contains('open'), true);
assert.equal(openButton.getAttribute('aria-expanded'), 'true');
assert.equal(document.activeElement, modalLinks[0]);

document.activeElement = modalLinks.at(-1);
event = await dispatchWindow('keydown', { key: 'Tab' });
assert.equal(event.defaultPrevented, true);
assert.equal(document.activeElement, closeButton);
document.activeElement = closeButton;
event = await dispatchWindow('keydown', { key: 'Tab', shiftKey: true });
assert.equal(event.defaultPrevented, true);
assert.equal(document.activeElement, modalLinks.at(-1));
await dispatchWindow('keydown', { key: 'Escape' });
assert.equal(modal.hidden, true);
assert.equal(modal.classList.contains('open'), false);
assert.equal(openButton.getAttribute('aria-expanded'), 'false');
assert.equal(document.activeElement, openButton, 'click trigger must regain focus');
assert.equal(modal.contains(document.activeElement), false);

origin.focus();
event = await dispatchWindow('keydown', { key: 'k', metaKey: true });
assert.equal(event.defaultPrevented, true);
assert.equal(modal.hidden, false);
await dispatchWindow('keydown', { key: 'k', metaKey: true });
assert.equal(modal.hidden, true);
assert.equal(document.activeElement, origin, 'Cmd+K toggle must restore focusable origin');

async function assertCopyCase(name, clipboardAction, execAction, expectedStatus, expectedLabel) {
  navigator.clipboard.writeText = clipboardAction;
  document.execCommand = execAction;
  copyStatus.textContent = '';
  copyButton.textContent = '复制微信号';
  let thrown = null;
  try { await copyButton.emit('click'); } catch (error) { thrown = error; }
  assert.equal(thrown, null, `${name}: handler must not reject`);
  assert.equal(copyStatus.textContent, expectedStatus, `${name}: status`);
  assert.equal(copyButton.textContent, expectedLabel, `${name}: label`);
  assert.equal(body.children.length, 0, `${name}: temporary textarea cleanup`);
}

await assertCopyCase('Clipboard API success', async () => {}, () => { throw new Error('execCommand must not run'); }, '微信号已复制，可以直接添加。', '已复制 ✓');
await assertCopyCase('execCommand success', async () => { throw new Error('clipboard denied'); }, () => true, '微信号已复制，可以直接添加。', '已复制 ✓');
await assertCopyCase('execCommand false', async () => { throw new Error('clipboard denied'); }, () => false, '微信号：wang1227928718', '复制微信号');
await assertCopyCase('execCommand throws', async () => { throw new Error('clipboard denied'); }, () => { throw new Error('legacy copy denied'); }, '微信号：wang1227928718', '复制微信号');

assert.match(String(year.textContent), /^\d{4}$/);
console.log('dynamic interactions: OK (filters, modal focus/state, keyboard, clipboard fallbacks)');
