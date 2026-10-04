"use strict";

(() => {
  let syncPreview = () => {};
  const reducedMotion = () => typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
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

      syncPreview();
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
  const exhibit = document.querySelector(".ledger-exhibit");
  const preview = document.querySelector("#ledger-preview");
  const catalogNode = document.querySelector("#project-data");
  const catalog = new Map(catalogNode ? JSON.parse(catalogNode.textContent).map(p => [String(p.id), p]) : []);
  let previewId;
  let previewAnimation;
  const setPreview = row => {
    if (!preview || !row) return;
    const p = catalog.get(row.dataset.ledgerId);
    if (!p || previewId === String(p.id)) return;
    previewId = String(p.id);
    const img = document.querySelector("#preview-image");
    img.src = p.image; img.alt = `${p.name} 项目预览`;
    document.querySelector("#preview-title").textContent = p.name;
    document.querySelector("#preview-summary").textContent = p.summary;
    const button = preview.querySelector("[data-project-open]");
    button.dataset.projectOpen = String(p.id);
    button.setAttribute("aria-label", `查看 ${p.name} 项目详情`);
    rows.forEach(item => item.classList.toggle("is-previewed", item === row));
    if (previewAnimation) previewAnimation.cancel();
    if (!reducedMotion() && typeof img.animate === "function" && !preview.hidden) {
      previewAnimation = img.animate([{opacity: .25, transform: "translateY(8px)"}, {opacity: 1, transform: "translateY(0)"}], {duration: 220, easing: "ease-out"});
    }
  };
  syncPreview = () => {
    if (!preview) return;
    const visible = rows.filter(row => !row.hidden);
    preview.hidden = !exhibit.classList.contains("is-exhibit") || !visible.length;
    if (!visible.some(row => row.dataset.ledgerId === previewId)) setPreview(visible[0]);
  };
  if (viewSwitch && wall && viewButtons.length) {
    viewSwitch.hidden = false;
    const selectView = view => {
      wall.classList.toggle("is-list", view === "list");
      if (exhibit) exhibit.classList.toggle("is-exhibit", view === "exhibit");
      viewButtons.forEach(item => item.setAttribute("aria-pressed", String(item.dataset.view === view)));
      syncPreview();
    };
    viewButtons.forEach(button => button.addEventListener("click", () => selectView(button.dataset.view)));
    if (preview) {
      rows.forEach(row => {
        row.addEventListener("pointerenter", () => setPreview(row));
        row.addEventListener("focusin", () => setPreview(row));
      });
      const desktop = window.matchMedia("(min-width: 1000px)");
      const adaptView = () => {
        const choice = viewButtons.find(button => button.dataset.view === "exhibit");
        choice.hidden = !desktop.matches;
        if (desktop.matches) selectView("exhibit");
        else if (exhibit.classList.contains("is-exhibit")) selectView("wall");
      };
      desktop.addEventListener("change", adaptView);
      adaptView();
    }
  }

  const dialog = document.querySelector("#project-dialog");
  const projectData = document.querySelector("#project-data");
  if (dialog && projectData && typeof dialog.showModal === "function") {
    const projects = catalog;
    const labels = {ai: "AI 产品", game: "游戏与内容", tool: "实用工具", creative: "创意实验"};
    const close = document.querySelector("#detail-close");
    let opener;
    const put = (id, value) => { document.querySelector(`#detail-${id}`).textContent = value; };
    const openProject = (id, trigger) => {
      const project = projects.get(id);
      if (!project) return;
      opener = trigger;
      const sourceImage = trigger.querySelector("img");
      const sourceRect = sourceImage ? sourceImage.getBoundingClientRect() : trigger.getBoundingClientRect();
      const detailImage = document.querySelector("#detail-image");
      detailImage.src = project.image; detailImage.alt = `${project.name} 真实页面截图`;
      document.querySelector(".detail-media").hidden = false;
      put("domain", new URL(project.url).hostname);
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
      if (!reducedMotion() && typeof detailImage.animate === "function") {
        const target = detailImage.getBoundingClientRect();
        const scale = Math.max(.25, Math.min(1, sourceRect.width / target.width));
        detailImage.animate([
          {transform: `translate(${sourceRect.left-target.left}px,${sourceRect.top-target.top}px) scale(${scale})`, opacity: .4},
          {transform: "translate(0,0) scale(1)", opacity: 1}
        ], {duration: 380, easing: "cubic-bezier(.2,.8,.2,1)"});
      }
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
    document.querySelectorAll("[data-project-open]").forEach(trigger => {
      trigger.setAttribute("aria-haspopup", "dialog");
      trigger.addEventListener("click", event => {
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button > 0) return;
        event.preventDefault(); openProject(trigger.dataset.projectOpen, trigger);
      });
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

  const hero = document.querySelector(".hero");
  const scene = document.querySelector(".hero-scene");
  if (hero && scene && typeof window !== "undefined") {
    const desktop = window.matchMedia("(min-width: 1000px)");
    const motion = window.matchMedia("(prefers-reduced-motion: reduce)");
    const finePointer = window.matchMedia("(pointer: fine)");
    let frame = 0;
    let pointerX = 0, pointerY = 0;
    const paint = () => {
      frame = 0;
      const enabled = desktop.matches && !motion.matches;
      hero.classList.toggle("has-scroll-scene", enabled);
      const rect = hero.getBoundingClientRect();
      const progress = enabled ? Math.max(0, Math.min(1, -rect.top / 360)) : 0;
      scene.style.setProperty("--g", progress.toFixed(4));
      scene.style.setProperty("--pointer-x", `${enabled ? pointerX * (1-progress) : 0}px`);
      scene.style.setProperty("--pointer-y", `${enabled ? pointerY * (1-progress) : 0}px`);
    };
    const schedule = () => { if (!frame) frame = requestAnimationFrame(paint); };
    window.addEventListener("scroll", schedule, {passive: true});
    window.addEventListener("resize", schedule, {passive: true});
    motion.addEventListener("change", schedule);
    scene.addEventListener("pointermove", event => {
      if (!desktop.matches || motion.matches || !finePointer.matches) return;
      const rect = scene.getBoundingClientRect();
      pointerX = (event.clientX - rect.left - rect.width/2) * .014;
      pointerY = (event.clientY - rect.top - rect.height/2) * .014;
      schedule();
    });
    scene.addEventListener("pointerleave", () => { pointerX = 0; pointerY = 0; schedule(); });
    paint();
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
