const timeSelect = document.getElementById("select-time");
const createLinkBtn = document.getElementById("create-link-btn");
const copyContentBtn = document.getElementById("copy-content-btn");
const pageContentDiv = document.getElementById("page-content");

createLinkBtn.onclick = async () => {
  const url = await getPageUrl(pageContentDiv.innerText, timeSelect.value);
  await navigator.clipboard.writeText(url);
  alert("Url copied to clipboard");
};

copyContentBtn.onclick = async () => {
  await navigator.clipboard.writeText(pageContentDiv.innerText);
  alert("Content copied to clipboard");
};

pageContentDiv.oninput = async () => {
  isEmpty = pageContentDiv.innerText.length === 0;
  createLinkBtn.disabled = isEmpty;
  if (isEmpty) {
    createLinkBtn.classList.remove("btn-success");
    createLinkBtn.classList.add("btn-secondary");
  } else {
    createLinkBtn.classList.remove("btn-secondary");
    createLinkBtn.classList.add("btn-success");
  }
};
pageContentDiv.oninput();

async function getPageUrl(content, minutesLifetime) {
  const resp = await fetch("/api/pages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ content, minutes_lifetime: minutesLifetime }),
  });
  if (resp.status !== 201) {
    throw Error(`Failed to get resp, status=${resp.status}`);
  }
  const resp_data = await resp.json();
  return `${window.location.origin}/${resp_data.id}`;
}
