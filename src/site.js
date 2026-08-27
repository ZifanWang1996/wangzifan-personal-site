"use strict";

(() => {
  const rows = Array.from(document.querySelectorAll("[data-ledger-id]"));
  const filters = Array.from(document.querySelectorAll("[data-ledger-filter]"));
  const tools = document.querySelector(".ledger-tools");
  const search = document.querySelector("#ledger-search");
  const status = document.querySelector("#ledger-status");
  const count = document.querySelector("#ledger-count");
  const more = document.querySelector("#ledger-more");

  if (rows.length && filters.length && tools && search && status && count && more) {
    let category = "all";
    let expanded = false;

    const applyLedgerState = () => {
      const query = search.value.trim().toLowerCase();
      const selectedStatus = status.value;
      const matches = rows.filter((row) => {
        const categoryMatch = category === "all" || row.dataset.ledgerCategory === category;
        const statusMatch = selectedStatus === "all" || row.dataset.ledgerStatus === selectedStatus;
        const queryMatch = !query || row.dataset.ledgerSearch.includes(query);
        return categoryMatch && statusMatch && queryMatch;
      });
      const compactDefault = category === "all" && selectedStatus === "all" && !query && !expanded;
      const matchSet = new Set(matches);

      rows.forEach((row) => {
        const matchIndex = matches.indexOf(row);
        row.hidden = !matchSet.has(row) || (compactDefault && matchIndex >= 9);
      });

      count.textContent = `${matches.length} / ${rows.length}`;
      more.hidden = matches.length <= 9 || category !== "all" || selectedStatus !== "all" || Boolean(query);
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
    more.addEventListener("click", () => {
      expanded = !expanded;
      applyLedgerState();
    });

    applyLedgerState();
    tools.hidden = false;
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
