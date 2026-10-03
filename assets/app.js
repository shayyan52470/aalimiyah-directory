import { parseCSV, splitValues } from './csv.js';

const DATA_URL = 'data/courses.csv';

const LABELS = {
  id: 'ID', institution: 'Institution', programme_name: 'Programme', programme_type: 'Type',
  status: 'Status', delivery_mode: 'Delivery', institution_location: 'Institution location',
  country: 'Country', timezone: 'Timezone', languages: 'Languages', arabic_entry_level: 'Arabic entry level',
  gender: 'Gender', study_load: 'Study load', duration_years: 'Duration (years)', schedule: 'Schedule',
  curriculum: 'Curriculum', jurisprudence_school: 'School of law', theology_school: 'Theology',
  qualification: 'Qualification', accreditation: 'Accreditation', entry_requirements: 'Entry requirements',
  tuition_amount: 'Tuition amount', tuition_currency: 'Currency', tuition_period: 'Tuition period',
  tuition_notes: 'Tuition notes', financial_aid: 'Financial aid', subjects: 'Subjects', texts: 'Texts',
  tags: 'Tags', official_url: 'Official URL', syllabus_url: 'Syllabus URL', source_urls: 'Source URLs',
  last_verified: 'Last verified', notes: 'Notes'
};

const DEFAULT_COLUMNS = [
  'institution', 'programme_name', 'status', 'delivery_mode', 'country', 'languages',
  'study_load', 'duration_years', 'jurisprudence_school', 'subjects', 'last_verified'
];

async function loadRows() {
  const response = await fetch(DATA_URL, { cache: 'no-store' });
  if (!response.ok) throw new Error(`CSV request failed: ${response.status}`);
  return parseCSV(await response.text());
}

function unique(rows, field, multi = false) {
  const values = rows.flatMap((row) => multi ? splitValues(row[field]) : [row[field]])
    .map((value) => value.trim()).filter(Boolean);
  return [...new Set(values)].sort((a, b) => a.localeCompare(b, undefined, { sensitivity: 'base' }));
}

function addOptions(select, values) {
  values.forEach((value) => select.add(new Option(value, value)));
}

function titleCase(value) {
  return String(value || '').replaceAll('-', ' ').replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function normal(value) {
  return String(value || '').toLocaleLowerCase();
}

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function createCourseCard(row) {
  const article = el('article', 'course-card');
  article.append(el('p', 'institution', row.institution));
  article.append(el('h3', '', row.programme_name || 'Programme details in progress'));

  const meta = el('div', 'meta-list');
  [row.delivery_mode, row.study_load, row.duration_years && `${row.duration_years} years`, row.country]
    .filter(Boolean).forEach((item) => meta.append(el('span', '', titleCase(item))));
  article.append(meta);

  const chips = el('ul', 'chips');
  const highlighted = [
    ...splitValues(row.languages),
    ...splitValues(row.jurisprudence_school),
    ...splitValues(row.subjects).slice(0, 4)
  ].slice(0, 7);
  highlighted.forEach((item) => chips.append(el('li', 'chip', item)));
  article.append(chips);

  const footer = document.createElement('footer');
  footer.append(el('span', '', row.last_verified ? `Checked ${row.last_verified}` : 'Verification date pending'));
  if (row.official_url) {
    const link = el('a', '', 'View programme →');
    link.href = row.official_url;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    footer.append(link);
  }
  article.append(footer);
  return article;
}

async function initDirectory() {
  const grid = document.querySelector('#course-grid');
  try {
    const allRows = await loadRows();
    const rows = allRows.filter((row) => row.status === 'published');
    document.querySelector('#programme-count').textContent = rows.length;
    document.querySelector('#country-count').textContent = unique(rows, 'country').length;
    document.querySelector('#online-count').textContent = rows.filter((row) => row.delivery_mode === 'online' || row.delivery_mode === 'hybrid').length;

    const controls = {
      search: document.querySelector('#search'), delivery: document.querySelector('#delivery'),
      load: document.querySelector('#study-load'), language: document.querySelector('#language'),
      school: document.querySelector('#school'), subject: document.querySelector('#subject')
    };
    addOptions(controls.delivery, unique(rows, 'delivery_mode'));
    addOptions(controls.load, unique(rows, 'study_load'));
    addOptions(controls.language, unique(rows, 'languages', true));
    addOptions(controls.school, unique(rows, 'jurisprudence_school', true));
    addOptions(controls.subject, unique(rows, 'subjects', true));

    function render() {
      const query = normal(controls.search.value.trim());
      const selected = {
        delivery: controls.delivery.value, load: controls.load.value, language: controls.language.value,
        school: controls.school.value, subject: controls.subject.value
      };
      const filtered = rows.filter((row) => {
        const haystack = normal(Object.values(row).join(' '));
        return (!query || haystack.includes(query)) &&
          (!selected.delivery || row.delivery_mode === selected.delivery) &&
          (!selected.load || row.study_load === selected.load) &&
          (!selected.language || splitValues(row.languages).includes(selected.language)) &&
          (!selected.school || splitValues(row.jurisprudence_school).includes(selected.school)) &&
          (!selected.subject || splitValues(row.subjects).includes(selected.subject));
      });
      grid.replaceChildren(...filtered.map(createCourseCard));
      if (!filtered.length) {
        const empty = el('div', 'empty-state');
        empty.append(el('h3', '', 'No programmes match those filters'));
        empty.append(el('p', '', 'Try removing a filter or using a broader search term.'));
        grid.append(empty);
      }
      document.querySelector('#result-count').textContent = `${filtered.length} ${filtered.length === 1 ? 'programme' : 'programmes'}`;
      const activeCount = Object.values(selected).filter(Boolean).length + (query ? 1 : 0);
      document.querySelector('#active-filter-summary').textContent = activeCount ? `· ${activeCount} active ${activeCount === 1 ? 'filter' : 'filters'}` : '';
      grid.setAttribute('aria-busy', 'false');
    }

    Object.values(controls).forEach((control) => control.addEventListener(control.tagName === 'INPUT' ? 'input' : 'change', render));
    document.querySelector('#directory-filters').addEventListener('reset', () => window.setTimeout(render));
    render();
  } catch (error) {
    console.error(error);
    grid.setAttribute('aria-busy', 'false');
    document.querySelector('#directory-error').hidden = false;
    document.querySelector('#result-count').textContent = 'Unavailable';
  }
}

function renderCell(field, value) {
  const td = document.createElement('td');
  td.title = value;
  if (field === 'status') {
    td.append(el('span', `status-pill ${value}`, titleCase(value)));
  } else if (field.endsWith('_url') && value) {
    const link = el('a', '', 'Open link');
    link.href = value;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    td.append(link);
  } else if (field === 'source_urls' && value) {
    const values = splitValues(value);
    values.forEach((url, index) => {
      const link = el('a', '', `Source ${index + 1}`);
      link.href = url; link.target = '_blank'; link.rel = 'noopener noreferrer';
      if (index) td.append(document.createTextNode(' · '));
      td.append(link);
    });
  } else {
    td.textContent = value || '—';
  }
  return td;
}

async function initDataExplorer() {
  const table = document.querySelector('#data-table');
  try {
    const rows = await loadRows();
    const fields = Object.keys(rows[0] || LABELS);
    const visible = new Set(DEFAULT_COLUMNS);
    const controls = {
      search: document.querySelector('#data-search'), status: document.querySelector('#status-filter'),
      tag: document.querySelector('#tag-filter')
    };
    addOptions(controls.status, unique(rows, 'status'));
    addOptions(controls.tag, unique(rows, 'tags', true));

    const fieldset = document.querySelector('#column-options');
    fields.forEach((field) => {
      const label = document.createElement('label');
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox'; checkbox.value = field; checkbox.checked = visible.has(field);
      checkbox.addEventListener('change', () => { checkbox.checked ? visible.add(field) : visible.delete(field); render(); });
      label.append(checkbox, document.createTextNode(LABELS[field] || titleCase(field)));
      fieldset.append(label);
    });

    let sortField = 'institution';
    let sortDirection = 1;

    function render() {
      const query = normal(controls.search.value.trim());
      const filtered = rows.filter((row) =>
        (!query || normal(Object.values(row).join(' ')).includes(query)) &&
        (!controls.status.value || row.status === controls.status.value) &&
        (!controls.tag.value || splitValues(row.tags).includes(controls.tag.value))
      ).sort((a, b) => String(a[sortField]).localeCompare(String(b[sortField]), undefined, { numeric: true, sensitivity: 'base' }) * sortDirection);

      const shown = fields.filter((field) => visible.has(field));
      const headerRow = document.createElement('tr');
      shown.forEach((field) => {
        const th = document.createElement('th');
        const button = el('button', '', `${LABELS[field] || titleCase(field)}${sortField === field ? (sortDirection === 1 ? ' ↑' : ' ↓') : ''}`);
        button.type = 'button';
        button.addEventListener('click', () => {
          if (sortField === field) sortDirection *= -1; else { sortField = field; sortDirection = 1; }
          render();
        });
        th.append(button); headerRow.append(th);
      });
      table.tHead.replaceChildren(headerRow);
      table.tBodies[0].replaceChildren(...filtered.map((row) => {
        const tr = document.createElement('tr');
        shown.forEach((field) => tr.append(renderCell(field, row[field])));
        return tr;
      }));
      document.querySelector('#data-count').textContent = `${filtered.length} of ${rows.length} records`;
    }

    controls.search.addEventListener('input', render);
    controls.status.addEventListener('change', render);
    controls.tag.addEventListener('change', render);
    render();
  } catch (error) {
    console.error(error);
    document.querySelector('#data-error').hidden = false;
    document.querySelector('#data-count').textContent = 'Unavailable';
  }
}

const page = document.body.dataset.page;
if (page === 'directory') initDirectory();
if (page === 'data') initDataExplorer();

