"use strict";

(() => {
  const rows = Array.from(document.querySelectorAll("[data-ledger-id]"));
  const filters = Array.from(document.querySelectorAll("[data-ledger-filter]"));
  const tools = document.querySelector(".ledger-tools");
  const search = document.querySelector("#ledger-search");
  const status = document.querySelector("#ledger-status");
  const period = document.querySelector("#ledger-period");
  const count = document.querySelector("#ledger-count");
  const empty = document.querySelector("#ledger-empty");
  const more = document.querySelector("#ledger-more");

  if (rows.length && filters.length && tools && search && status && count && empty && more) {
    let category = "all";
    let expanded = false;

    const applyLedgerState = () => {
      const query = search.value.trim().toLowerCase();
      const selectedStatus = status.value;
      const selectedPeriod = period ? period.value : "all";
      const matches = rows.filter((row) => {
        const categoryMatch = category === "all" || row.dataset.ledgerCategory === category;
        const statusMatch = selectedStatus === "all" || row.dataset.ledgerStatus === selectedStatus;
        const queryMatch = !query || row.dataset.ledgerSearch.includes(query);
        const periodMatch = selectedPeriod === "all" || row.dataset.ledgerPeriod.startsWith(selectedPeriod);
        return categoryMatch && statusMatch && queryMatch && periodMatch;
      });
      const compactDefault = category === "all" && selectedStatus === "all" && !query && selectedPeriod === "all" && !expanded;
      const matchSet = new Set(matches);

      rows.forEach((row) => {
        const matchIndex = matches.indexOf(row);
        row.hidden = !matchSet.has(row) || (compactDefault && matchIndex >= 9);
      });

      count.textContent = `${matches.length} / ${rows.length}`;
      empty.hidden = matches.length !== 0;
      more.hidden = matches.length <= 9 || category !== "all" || selectedStatus !== "all" || Boolean(query) || selectedPeriod !== "all";
      const collection = document.querySelector("#ledger-list");
      if (collection) collection.classList.toggle("is-filtered", category !== "all" || selectedStatus !== "all" || Boolean(query) || selectedPeriod !== "all");
      more.setAttribute("aria-expanded", String(expanded));
      more.textContent = expanded ? "收起发布档案" : `查看全部 ${rows.length} 条记录`;
    };

    filters.forEach((filter) => {
      filter.addEventListener("click", () => {
        category = filter.dataset.ledgerFilter;
        expanded = false;
        filters.forEach((item) => {
          const active = item === filter;
          item.classList.toggle("is-active", active);
          item.setAttribute("aria-pressed", String(active));
        });
        applyLedgerState();
      });
    });

    search.addEventListener("input", () => {
      expanded = false;
      applyLedgerState();
    });
    status.addEventListener("change", () => {
      expanded = false;
      applyLedgerState();
    });
    if (period) period.addEventListener("change", () => { expanded = false; applyLedgerState(); });
    more.addEventListener("click", () => {
      expanded = !expanded;
      applyLedgerState();
    });

    const revealFragment = () => {
      const id = typeof window !== "undefined" ? window.location.hash.slice(1) : "";
      const target = rows.find(row => `project-${row.dataset.ledgerId}` === id);
      if (!target) return;
      category = "all"; expanded = true; search.value = ""; status.value = "all";
      if (period) period.value = "all";
      filters.forEach(item => {
        const active = item.dataset.ledgerFilter === "all";
        item.classList.toggle("is-active", active); item.setAttribute("aria-pressed", String(active));
      });
      applyLedgerState();
      target.scrollIntoView({block: "start"});
      const main = target.querySelector(".ledger-main");
      if (main) main.focus({preventScroll: true});
    };
    if (typeof window !== "undefined") {
      window.addEventListener("hashchange", revealFragment);
      document.querySelectorAll('a[href^="#project-"]').forEach(link => link.addEventListener("click", () => {
        if (window.location.hash === link.getAttribute("href")) revealFragment();
      }));
    }
    applyLedgerState();
    revealFragment();
    tools.hidden = false;
  }

  const viewSwitch = document.querySelector(".view-switch");
  const wall = document.querySelector("#ledger-list");
  const viewButtons = Array.from(document.querySelectorAll("[data-view]"));
  if (viewSwitch && wall && viewButtons.length) {
    viewSwitch.hidden = false;
    viewButtons.forEach((button) => {
      button.addEventListener("click", () => {
        wall.classList.toggle("is-list", button.dataset.view === "list");
        viewButtons.forEach((item) => {
          item.setAttribute("aria-pressed", String(item === button));
        });
      });
    });
  }

  const dialog = document.querySelector("#project-dialog");
  const projectData = document.querySelector("#project-data");
  if (dialog && projectData && typeof dialog.showModal === "function") {
    const projects = new Map(JSON.parse(projectData.textContent).map(project => [String(project.id), project]));
    const labels = {ai: "AI 产品", game: "游戏与内容", tool: "实用工具", creative: "创意实验"};
    const close = document.querySelector("#detail-close");
    let opener;
    const put = (id, value) => { document.querySelector(`#detail-${id}`).textContent = value; };
    const openProject = (id, trigger) => {
      const project = projects.get(id);
      if (!project) return;
      opener = trigger;
      put("number", String(project.id).padStart(2, "0"));
      put("category", labels[project.category]);
      ["name", "subtitle", "summary", "problem", "solution", "evidence"].forEach(key => put(key === "name" ? "title" : key, project[key]));
      put("date", project.launched_at);
      put("status", project.status === "live" ? "在线记录" : "离线记录");
      document.querySelector("#detail-problem-wrap").hidden = project.problem.startsWith("把“");
      document.querySelector("#detail-solution-wrap").hidden = project.solution === project.summary;
      const visit = document.querySelector("#detail-visit");
      visit.replaceChildren();
      if (project.status === "live") {
        const link = document.createElement("a");
        link.href = project.url; link.target = "_blank"; link.rel = "noopener noreferrer";
        link.className = "button button-primary"; link.textContent = "访问项目网站 ↗";
        visit.append(link);
      } else {
        const note = document.createElement("p"); note.textContent = "这是一个保留的离线档案，暂不提供访问入口。"; visit.append(note);
      }
      dialog.showModal(); dialog.scrollTop = 0; close.focus({preventScroll: true});
    };
    rows.forEach(row => {
      const trigger = row.querySelector(".ledger-main");
      if (!trigger) return;
      trigger.setAttribute("aria-haspopup", "dialog");
      const caption = row.querySelector(".card-read");
      if (caption) caption.textContent = "项目故事 ↗";
      trigger.addEventListener("click", event => {
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button > 0) return;
        event.preventDefault(); openProject(row.dataset.ledgerId, trigger);
      });
      if (row.dataset.ledgerStatus !== "live") {
        trigger.tabIndex = 0; trigger.setAttribute("role", "button");
        trigger.addEventListener("keydown", event => {
          if (event.key === "Enter" || event.key === " ") { event.preventDefault(); openProject(row.dataset.ledgerId, trigger); }
        });
      }
    });
    dialog.addEventListener("keydown", event => {
      if (event.key !== "Tab") return;
      const items = Array.from(dialog.querySelectorAll('a[href],button:not([disabled])')).filter(item => item.getClientRects().length);
      const first = items[0], last = items[items.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    });
    close.addEventListener("click", () => dialog.close());
    dialog.addEventListener("click", event => {
      if (event.target !== dialog) return;
      const r = dialog.getBoundingClientRect();
      if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close();
    });
    dialog.addEventListener("close", () => { if (opener) opener.focus({preventScroll: true}); });
  }

  const copyButton = document.querySelector("[data-copy-value]");
  const copyStatus = document.querySelector("#copy-status");
  const manualCopy = document.querySelector(".manual-copy");

  if (copyButton && copyStatus && manualCopy) {
    const manualInput = manualCopy.querySelector("input");
    copyButton.addEventListener("click", async () => {
      const value = copyButton.dataset.copyValue;
      let copied = false;

      try {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          await navigator.clipboard.writeText(value);
          copied = true;
        }
      } catch (_error) {
        copied = false;
      }

      if (!copied && manualInput) {
        manualCopy.hidden = false;
        manualInput.focus();
        manualInput.select();
        try {
          copied = document.execCommand("copy") === true;
        } catch (_error) {
          copied = false;
        }
      }

      if (copied) {
        manualCopy.hidden = true;
        copyButton.textContent = "已复制 ✓";
        copyStatus.textContent = "微信号已复制，可以直接添加。";
      } else {
        copyButton.textContent = "复制微信号";
        copyStatus.textContent = "复制失败，请在下方手动复制微信号。";
      }
    });
    copyButton.hidden = false;
  }
})();
