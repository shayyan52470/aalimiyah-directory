export function parseCSV(text) {
  const records = [];
  let row = [];
  let value = "";
  let quoted = false;

  for (let index = 0; index < text.length; index += 1) {
    const character = text[index];
    if (quoted) {
      if (character === '"' && text[index + 1] === '"') {
        value += '"';
        index += 1;
      } else if (character === '"') {
        quoted = false;
      } else {
        value += character;
      }
    } else if (character === '"') {
      quoted = true;
    } else if (character === ',') {
      row.push(value);
      value = "";
    } else if (character === '\n') {
      row.push(value.replace(/\r$/, ""));
      records.push(row);
      row = [];
      value = "";
    } else {
      value += character;
    }
  }

  if (value || row.length) {
    row.push(value.replace(/\r$/, ""));
    records.push(row);
  }

  const [headers = [], ...lines] = records.filter((record) => record.some((cell) => cell.trim()));
  return lines.map((line) => Object.fromEntries(headers.map((header, index) => [header, line[index] ?? ""])));
}

export function splitValues(value) {
  return String(value || "").split(';').map((item) => item.trim()).filter(Boolean);
}

