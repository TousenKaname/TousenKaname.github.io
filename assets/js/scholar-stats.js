/**
 * Renders Google Scholar data (gs_data.json, produced by
 * google_scholar_crawler/ and published on the `google-scholar-stats`
 * branch) into the homepage:
 *
 *   - total citation count            -> #total_cit
 *   - per-paper citation counts       -> .show_paper_citations[data]
 *   - auto-synced full publication list -> #gs-pub-list (+ #gs-pub-updated)
 *
 * Data fetching and wiring lives in _includes/fetch_google_scholar_stats.html.
 */

function gsEscapeHtml(value) {
    return String(value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
}

/* "A and B and C" -> "A, B, C", with the site owner's name emphasized. */
function gsFormatAuthors(authorString) {
    var authors = gsEscapeHtml(String(authorString).split(' and ').join(', '))
    return authors
        .replace(/\bGuoan Wang\b/g, '<strong>Guoan Wang</strong>')
        .replace(/\bG Wang\b/g, '<strong>G Wang</strong>')
}

function gsPublicationLink(pub) {
    if (pub['pub_url']) {
        return pub['pub_url']
    }
    var authorPubId = pub['author_pub_id'] || ''
    var scholarUser = authorPubId.split(':')[0]
    return 'https://scholar.google.com/citations?view_op=view_citation&hl=en&user='
        + scholarUser + '&citation_for_view=' + authorPubId
}

function gsPublicationVenue(pub) {
    var bib = pub['bib'] || {}
    return pub['venue'] || bib['journal'] || bib['conference'] || bib['book']
        || bib['source'] || bib['publisher'] || bib['citation'] || ''
}

/* Builds the year-grouped publication list, newest (then most cited) first. */
function gsBuildPubList(data) {
    var pubs = Object.keys(data['publications']).map(function (key) {
        return data['publications'][key]
    })
    pubs.sort(function (a, b) {
        var yearA = parseInt((a['bib'] || {})['pub_year'], 10) || 0
        var yearB = parseInt((b['bib'] || {})['pub_year'], 10) || 0
        if (yearB !== yearA) {
            return yearB - yearA
        }
        return (b['num_citations'] || 0) - (a['num_citations'] || 0)
    })

    var html = ''
    var currentYear = null
    pubs.forEach(function (pub) {
        var bib = pub['bib'] || {}
        var yearLabel = parseInt(bib['pub_year'], 10) ? String(parseInt(bib['pub_year'], 10)) : 'Others'
        if (yearLabel !== currentYear) {
            currentYear = yearLabel
            html += "<h3 class='gs-pub-year'>" + yearLabel + '</h3>'
        }

        html += "<div class='gs-pub-item'>"
        html += "<div class='gs-pub-title'><a href='" + gsEscapeHtml(gsPublicationLink(pub))
            + "' target='_blank' rel='noopener'>" + gsEscapeHtml(bib['title'] || 'Untitled') + '</a>'
        if (pub['num_citations'] > 0) {
            html += " <span class='gs-pub-cite'>" + pub['num_citations']
                + ' citation' + (pub['num_citations'] > 1 ? 's' : '') + '</span>'
        }
        html += '</div>'
        if (bib['author']) {
            html += "<div class='gs-pub-authors'>" + gsFormatAuthors(bib['author']) + '</div>'
        }
        var venue = gsPublicationVenue(pub)
        if (venue) {
            html += "<div class='gs-pub-venue'>" + gsEscapeHtml(venue) + '</div>'
        }
        html += '</div>'
    })
    return html
}

/* Entry point: applies every Scholar-driven element on the page. */
function gsRenderScholarData(data) {
    var totalCitEle = document.getElementById('total_cit')
    if (totalCitEle) {
        totalCitEle.innerHTML = data['citedby']
    }

    var citationEles = document.getElementsByClassName('show_paper_citations')
    Array.prototype.forEach.call(citationEles, function (element) {
        var paperId = element.getAttribute('data')
        if (data['publications'] && data['publications'][paperId]) {
            element.innerHTML = '| Citations: ' + data['publications'][paperId]['num_citations']
        }
    })

    var pubListEle = document.getElementById('gs-pub-list')
    if (pubListEle && data['publications']) {
        pubListEle.innerHTML = gsBuildPubList(data)
    }

    var updatedEle = document.getElementById('gs-pub-updated')
    if (updatedEle && data['updated']) {
        updatedEle.innerHTML = ' &middot; last updated ' + gsEscapeHtml(String(data['updated']).split(' ')[0])
    }
}

function gsShowPubListError() {
    var pubListEle = document.getElementById('gs-pub-list')
    if (pubListEle) {
        pubListEle.innerHTML = "<p class='gs-pub-note'>Could not load the publication list right now &mdash; "
            + "please visit my <a href='https://scholar.google.com/citations?user=avkysggAAAAJ' "
            + "target='_blank' rel='noopener'>Google Scholar profile</a> instead.</p>"
    }
}
