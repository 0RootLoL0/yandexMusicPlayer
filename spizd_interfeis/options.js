/**
 * Options script for Yandex Music player control.
 * Author Vitalii Rizo
 * http://squirrel-research.ru
 * https://github.com/vrizo/ya-music-controls
 * (c) 2016–2019
 * Yandex Music Player Control Plugin
 * v.1.7
 */

'use strict'

let notificationsCheckbox = document.getElementById('notifications')
let isMac = navigator.platform.indexOf('Mac') > -1
let ctrl = isMac ? 'Cmd' : 'Ctrl'
let bg = chrome.extension.getBackgroundPage()

let localizeUI = () => {
  for (let node of document.querySelectorAll('[data-i18n]')) {
    let code = node.dataset.i18n
    let text = browser.i18n.getMessage(code)
    node.appendChild(document.createTextNode(text))
  }
}

let format = combination => {
  if (!combination) return null
  let output = combination.replace(/\+/g, ' + ')
  if (isMac) output = output.replace('MacCtrl', 'Control')
  output = output.replace('Ctrl', ctrl)
  if (isMac) output = output.replace('Control', 'Ctrl')

  return output
}

let deformat = combination => {
  let output = combination.replace(/ +\+ +/g, '+')
  if (isMac) output = output.replace('Ctrl', 'MacCtrl')
  return output.replace(ctrl, 'Ctrl')
}

let validate = evt => {
  let combination = deformat(evt.target.value)
  let rule1 = new RegExp('^\\s*(Alt|Ctrl|Command|MacCtrl)\\s*\\+' +
    '\\s*(Shift\\s*\\+\\s*)?([A-Z0-9]|Comma|Period|Home|End|PageUp|' +
    'PageDown|Space|Insert|Delete|Up|Down|Left|Right)\\s*$')
  let rule2 = new RegExp('^\\s*((Alt|Ctrl|Command|MacCtrl)\\s*\\+' +
    '\\s*)?(Shift\\s*\\+\\s*)?(F[1-9]|F1[0-2])\\s*$')

  if (rule1.test(combination) || rule2.test(combination)) {
    evt.target.classList.remove('option__input-error')
  } else {
    evt.target.classList.add('option__input-error')
  }
}

let init = () => {
  if (isMac) {
    let cmds = document.querySelectorAll('.mac-only')
    cmds.forEach(elem => {
      elem.style = 'display: inline;'
    })
  }

  updateUI()
  localizeUI()
}

let updateUI = async function () {
  let commands = await browser.commands.getAll()
  let settings = browser.storage.local.get()

  settings.then(storage => {
    notificationsCheckbox.checked = storage.notifications || false
  })
  commands.forEach(command => {
    let input = document.getElementById(command.name)
    input.value = format(command.shortcut)
    input.placeholder = format(input.placeholder)
    input.addEventListener('keyup', evt => validate(evt))
  })
}

let updateNotifications = function () {
  let value = document.getElementById('notifications').checked
  bg.isNotificationsEnabled = value
  browser.storage.local.set({
    notifications: value
  })
}

let updateShortcut = async function () {
  let commands = await browser.commands.getAll()
  commands.forEach(command => {
    let input = document.getElementById(command.name)
    browser.commands.update({
      shortcut: deformat(input.value),
      name: command.name
    })
  })
}

let resetShortcut = async function () {
  if (confirm(browser.i18n.getMessage('optionsResetConfirm'))) {
    let commands = await browser.commands.getAll()
    commands.forEach(command => {
      browser.commands.reset(command.name)
    })
    updateUI()
  }
}

document.addEventListener('DOMContentLoaded', init)
notificationsCheckbox.addEventListener('change', updateNotifications)
document.getElementById('update').addEventListener('click', updateShortcut)
document.getElementById('reset').addEventListener('click', resetShortcut)
