// Arxiv Sanity Modern - Client-side Logic
// Replicates the filtering and interaction of the original

var papers = []; // Global paper data
var filter_timer = null;

function startFilter() {
    var q = document.getElementById('qfield').value;
    // Debounce
    if (filter_timer) { clearTimeout(filter_timer); }
    filter_timer = setTimeout(function () { filterPapers(q); }, 200);
}

function filterPapers(q) {
    var all_papers = document.getElementsByClassName('apaper');
    var n_total = all_papers.length;
    var n_shown = 0;

    q = q.toLowerCase();

    for (var i = 0; i < n_total; i++) {
        var p = all_papers[i];
        var title = p.getElementsByClassName('ts')[0].innerText.toLowerCase();
        var authors = p.getElementsByClassName('as')[0].innerText.toLowerCase();
        var abstract = p.getElementsByClassName('tt')[0].innerText.toLowerCase();

        if (q === '' || title.includes(q) || authors.includes(q) || abstract.includes(q)) {
            p.style.display = 'block';
            n_shown++;
        } else {
            p.style.display = 'none';
        }
    }

    // Update counter
    var count_div = document.getElementById('counter');
    if (count_div) {
        count_div.innerHTML = n_shown + ' / ' + n_total; // + ' papers shown';
    }
}

// BibTeX Logic
function toggleBibtex(pid) {
    var el = document.getElementById('bib_' + pid);
    if (el.style.display === 'none') {
        el.style.display = 'block';
    } else {
        el.style.display = 'none';
    }
}

// Initial setup
document.addEventListener("DOMContentLoaded", function () {
    var qf = document.getElementById('qfield');
    if (qf) {
        qf.addEventListener('keyup', startFilter);
    }
});
