const copyContentBtn = document.getElementById("copy-content-btn");
const pageContentDiv = document.getElementById("page-content");

copyContentBtn.onclick = async () => {
  await navigator.clipboard.writeText(pageContentDiv.value);
  alert("Content copied to clipboard");
};
