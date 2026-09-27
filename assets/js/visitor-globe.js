/**
 * Visitor globe (page footer): a slowly turning globe marking the countries
 * and regions this site's visitors come from, with the top five listed
 * beside it.
 *
 * Data: visitors.json on the `visitor-stats` branch, built by
 * visitor_crawler/ from the site's Flag Counter. Markup lives in
 * _includes/visitor-globe.html. The map libraries and world atlas are only
 * fetched once the globe scrolls near the viewport.
 *
 * Interaction: hover pauses the spin and shows a country's count, drag
 * turns the globe, and hovering a row of the top-five list turns the
 * globe to that country. Honors prefers-reduced-motion.
 */
(function () {
    var ACCENT = '0, 54, 159'   // $site-accent-color
    var MARKER = '240, 98, 56'  // warm contrast for visitor markers
    var D3_ARRAY = 'https://cdn.jsdelivr.net/npm/d3-array@3.2.4/dist/d3-array.min.js'
    var D3_GEO = 'https://cdn.jsdelivr.net/npm/d3-geo@3.1.1/dist/d3-geo.min.js'
    var TOPOJSON = 'https://cdn.jsdelivr.net/npm/topojson-client@3.1.0/dist/topojson-client.min.js'
    var ATLAS = 'https://cdn.jsdelivr.net/npm/world-atlas@2.0.2/countries-110m.json'
    var TILT = -18         // degrees; favors the northern hemisphere
    var SPIN = 0.006       // degrees per millisecond: one turn per minute
    var TOP_N = 5

    var root = document.getElementById('visitor-globe')
    if (!root) {
        return
    }
    var reduceMotion = window.matchMedia
        && window.matchMedia('(prefers-reduced-motion: reduce)').matches

    function formatNumber(value) {
        return Number(value).toLocaleString('en-US')
    }

    function escapeHtml(value) {
        return String(value)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
    }

    function loadScript(src) {
        return new Promise(function (resolve, reject) {
            var script = document.createElement('script')
            script.src = src
            script.onload = resolve
            script.onerror = function () {
                reject(new Error('Could not load ' + src))
            }
            document.head.appendChild(script)
        })
    }

    function fetchJson(url) {
        return fetch(url).then(function (resp) {
            if (!resp.ok) {
                throw new Error(url + ' returned ' + resp.status)
            }
            return resp.json()
        })
    }

    /* Totals, top-five list and "updated" date beside the globe. */
    function renderSummary(data, onFocus) {
        var countries = data.countries
        var max = countries[0].visitors

        var totals = root.querySelector('.visitor-globe__totals')
        totals.innerHTML = '<strong>' + formatNumber(data.total_visitors) + '</strong> visitors from <strong>'
            + countries.length + '</strong> countries &amp; regions'
        totals.hidden = false

        var list = root.querySelector('.visitor-globe__top')
        list.innerHTML = countries.slice(0, TOP_N).map(function (country, index) {
            return "<li data-index='" + index + "'>"
                + "<span class='visitor-globe__name'>" + escapeHtml(country.name) + '</span>'
                + "<span class='visitor-globe__bar'><span style='width:"
                + Math.max(2, 100 * country.visitors / max).toFixed(1) + "%'></span></span>"
                + "<span class='visitor-globe__count'>" + formatNumber(country.visitors) + '</span>'
                + '</li>'
        }).join('')
        list.hidden = false
        Array.prototype.forEach.call(list.children, function (item) {
            var country = countries[+item.getAttribute('data-index')]
            item.addEventListener('mouseenter', function () { onFocus(country) })
            item.addEventListener('mouseleave', function () { onFocus(null) })
        })

        var updated = new Date(data.updated)
        if (!isNaN(updated)) {
            root.querySelector('.visitor-globe__updated').textContent = 'Updated '
                + updated.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
        }
    }

    function createGlobe(world, countries) {
        var stage = root.querySelector('.visitor-globe__stage')
        var canvas = stage.querySelector('canvas')
        var tip = stage.querySelector('.visitor-globe__tip')
        var ctx = canvas.getContext('2d')

        var sphere = { type: 'Sphere' }
        var graticule = d3.geoGraticule10()
        var land = topojson.feature(world, world.objects.countries)
        var borders = topojson.mesh(world, world.objects.countries)
        var featureById = {}
        land.features.forEach(function (feature) {
            featureById[feature.id] = feature
        })

        var markers = countries.filter(function (country) {
            return typeof country.lat === 'number'
        })
        var max = countries.length ? countries[0].visitors : 1
        var shaded = countries.filter(function (country) {
            return featureById[country.iso_n3]
        }).map(function (country) {
            var share = Math.log(1 + country.visitors) / Math.log(1 + max)
            return { feature: featureById[country.iso_n3], alpha: 0.16 + 0.5 * share }
        })

        var projection = d3.geoOrthographic().clipAngle(90).precision(0.6)
        var path = d3.geoPath(projection, ctx)
        var start = markers.length ? markers[0].lon : 0
        var rotation = [-start, TILT, 0]
        var size = 0
        var radius = 0

        var active = null      // country under the pointer / focused in the list
        var focusTarget = null // rotation the globe is easing towards
        var pointerInside = false
        var drag = null
        var visible = false
        var frame = 0
        var last = 0

        function markerRadius(country) {
            return Math.max(1.4, (1.6 + 4.4 * Math.sqrt(country.visitors / max)) * size / 190)
        }

        function viewCenter() {
            return [-rotation[0], -rotation[1]]
        }

        function resize() {
            size = stage.clientWidth
            var ratio = window.devicePixelRatio || 1
            canvas.width = Math.round(size * ratio)
            canvas.height = Math.round(size * ratio)
            ctx.setTransform(ratio, 0, 0, ratio, 0, 0)
            radius = size / 2 * 0.9
            projection.scale(radius).translate([size / 2, size / 2])
        }

        function render(now) {
            var middle = size / 2
            projection.rotate(rotation)
            ctx.clearRect(0, 0, size, size)

            // soft atmosphere around the rim
            var halo = ctx.createRadialGradient(middle, middle, radius * 0.92, middle, middle, size / 2)
            halo.addColorStop(0, 'rgba(' + ACCENT + ', 0.14)')
            halo.addColorStop(1, 'rgba(' + ACCENT + ', 0)')
            ctx.fillStyle = halo
            ctx.beginPath()
            ctx.arc(middle, middle, size / 2, 0, 2 * Math.PI)
            ctx.fill()

            // ocean, lit from the upper left
            var ocean = ctx.createRadialGradient(middle - radius * 0.35, middle - radius * 0.4, radius * 0.05,
                middle, middle, radius)
            ocean.addColorStop(0, '#fbfdff')
            ocean.addColorStop(1, '#d6e1f2')
            ctx.beginPath()
            path(sphere)
            ctx.fillStyle = ocean
            ctx.fill()

            ctx.beginPath()
            path(graticule)
            ctx.strokeStyle = 'rgba(' + ACCENT + ', 0.07)'
            ctx.lineWidth = 0.5
            ctx.stroke()

            ctx.beginPath()
            path(land)
            ctx.fillStyle = '#ffffff'
            ctx.fill()

            // visited countries, deeper blue for more visitors
            shaded.forEach(function (item) {
                ctx.beginPath()
                path(item.feature)
                ctx.fillStyle = 'rgba(' + ACCENT + ', ' + item.alpha.toFixed(3) + ')'
                ctx.fill()
            })

            ctx.beginPath()
            path(borders)
            ctx.strokeStyle = 'rgba(' + ACCENT + ', 0.2)'
            ctx.lineWidth = 0.5
            ctx.stroke()

            if (active && featureById[active.iso_n3]) {
                ctx.beginPath()
                path(featureById[active.iso_n3])
                ctx.strokeStyle = 'rgba(' + ACCENT + ', 0.85)'
                ctx.lineWidth = 1.2
                ctx.stroke()
            }

            // markers, largest first so small ones stay on top
            var center = viewCenter()
            markers.forEach(function (country, index) {
                var distance = d3.geoDistance([country.lon, country.lat], center)
                if (distance > Math.PI / 2) {
                    return
                }
                var point = projection([country.lon, country.lat])
                var fade = Math.min(1, (Math.PI / 2 - distance) / 0.3)
                var r = markerRadius(country)
                if (!reduceMotion && index < TOP_N) {
                    var phase = (now / 2400 + index / TOP_N) % 1
                    ctx.beginPath()
                    ctx.arc(point[0], point[1], r * (1 + 2 * phase), 0, 2 * Math.PI)
                    ctx.strokeStyle = 'rgba(' + MARKER + ', ' + (0.55 * (1 - phase) * fade).toFixed(3) + ')'
                    ctx.lineWidth = 1.2
                    ctx.stroke()
                }
                ctx.beginPath()
                ctx.arc(point[0], point[1], r, 0, 2 * Math.PI)
                ctx.fillStyle = 'rgba(' + MARKER + ', ' + (0.92 * fade).toFixed(3) + ')'
                ctx.fill()
                ctx.lineWidth = country === active ? 2 : 1
                ctx.strokeStyle = 'rgba(255, 255, 255, ' + fade.toFixed(3) + ')'
                ctx.stroke()
            })

            ctx.beginPath()
            path(sphere)
            ctx.strokeStyle = 'rgba(' + ACCENT + ', 0.22)'
            ctx.lineWidth = 1
            ctx.stroke()

            placeTip()
        }

        function placeTip() {
            if (!active || d3.geoDistance([active.lon, active.lat], viewCenter()) > Math.PI / 2) {
                tip.hidden = true
                return
            }
            var point = projection([active.lon, active.lat])
            tip.innerHTML = '<strong>' + escapeHtml(active.name) + '</strong> '
                + formatNumber(active.visitors) + ' visitor' + (active.visitors === 1 ? '' : 's')
            tip.hidden = false
            var half = tip.offsetWidth / 2
            tip.style.left = Math.min(Math.max(point[0], half), size - half) + 'px'
            tip.style.top = (point[1] - markerRadius(active) - 6) + 'px'
        }

        function tick(now) {
            frame = 0
            var elapsed = last ? Math.min(now - last, 50) : 0
            last = now
            if (focusTarget) {
                var dLon = ((focusTarget[0] - rotation[0]) % 360 + 540) % 360 - 180
                rotation[0] += dLon * 0.12
                rotation[1] += (focusTarget[1] - rotation[1]) * 0.12
            } else if (!drag && !pointerInside && !active) {
                rotation[0] += elapsed * SPIN
            }
            render(now)
            schedule()
        }

        function schedule() {
            if (frame || !visible || document.hidden) {
                return
            }
            if (reduceMotion && !focusTarget) {
                render(0)
                return
            }
            frame = requestAnimationFrame(tick)
        }

        function redraw() {
            if (reduceMotion) {
                if (focusTarget) {
                    rotation = [focusTarget[0], focusTarget[1], 0]
                    focusTarget = null
                }
                render(0)
            } else {
                schedule()
            }
        }

        /* Country under a canvas point: nearest marker, else visited land. */
        function hitTest(x, y) {
            var center = viewCenter()
            var best = null
            var bestDistance = Infinity
            markers.forEach(function (country) {
                if (d3.geoDistance([country.lon, country.lat], center) > Math.PI / 2 - 0.05) {
                    return
                }
                var point = projection([country.lon, country.lat])
                var distance = Math.hypot(point[0] - x, point[1] - y)
                if (distance < Math.max(8, markerRadius(country) + 3) && distance < bestDistance) {
                    best = country
                    bestDistance = distance
                }
            })
            if (best || Math.hypot(x - size / 2, y - size / 2) > radius) {
                return best
            }
            var location = projection.invert([x, y])
            for (var i = 0; i < countries.length; i++) {
                var feature = featureById[countries[i].iso_n3]
                if (feature && typeof countries[i].lat === 'number' && d3.geoContains(feature, location)) {
                    return countries[i]
                }
            }
            return null
        }

        function pointAt(event) {
            var rect = canvas.getBoundingClientRect()
            return [event.clientX - rect.left, event.clientY - rect.top]
        }

        canvas.addEventListener('pointerenter', function (event) {
            if (event.pointerType === 'mouse') {
                pointerInside = true
            }
        })
        canvas.addEventListener('pointerleave', function (event) {
            if (event.pointerType === 'mouse') {
                pointerInside = false
                active = null
                redraw()
            }
        })
        canvas.addEventListener('pointerdown', function (event) {
            drag = { x: event.clientX, y: event.clientY, rotation: rotation.slice(), moved: false }
            canvas.setPointerCapture(event.pointerId)
        })
        canvas.addEventListener('pointermove', function (event) {
            if (drag) {
                var dx = event.clientX - drag.x
                var dy = event.clientY - drag.y
                if (Math.abs(dx) + Math.abs(dy) > 3) {
                    drag.moved = true
                    active = null
                }
                var degreesPerPixel = 70 / radius
                rotation[0] = drag.rotation[0] + dx * degreesPerPixel
                rotation[1] = Math.max(-70, Math.min(70, drag.rotation[1] - dy * degreesPerPixel))
                redraw()
            } else if (event.pointerType === 'mouse') {
                var point = pointAt(event)
                var hit = hitTest(point[0], point[1])
                if (hit !== active) {
                    active = hit
                    canvas.style.cursor = hit ? 'pointer' : ''
                    redraw()
                }
            }
        })
        function endDrag(event) {
            // a tap (no drag) on touch screens toggles the country's label
            if (drag && !drag.moved && event.type === 'pointerup' && event.pointerType !== 'mouse') {
                var point = pointAt(event)
                active = hitTest(point[0], point[1])
            }
            drag = null
            redraw()
        }
        canvas.addEventListener('pointerup', endDrag)
        canvas.addEventListener('pointercancel', endDrag)

        document.addEventListener('visibilitychange', function () {
            last = 0
            redraw()
        })
        window.addEventListener('resize', function () {
            resize()
            redraw()
        })
        if ('IntersectionObserver' in window) {
            new IntersectionObserver(function (entries) {
                visible = entries[0].isIntersecting
                last = 0
                redraw()
            }).observe(stage)
        } else {
            visible = true
        }

        resize()
        render(0)
        schedule()

        return {
            focus: function (country) {
                active = country && typeof country.lat === 'number' ? country : null
                focusTarget = active ? [-active.lon, Math.max(-60, Math.min(60, -active.lat * 0.8))] : null
                redraw()
            }
        }
    }

    function start() {
        var dataRequest = fetchJson(root.getAttribute('data-src') + '?ts=' + Date.now())
            .then(function (data) {
                return data && data.countries && data.countries.length ? data : null
            })
            .catch(function () { return null })
        var globe = null

        dataRequest.then(function (data) {
            if (data) {
                renderSummary(data, function (country) {
                    if (globe) {
                        globe.focus(country)
                    }
                })
            }
        })

        var mapRequest = Promise.all([
            loadScript(D3_ARRAY).then(function () { return loadScript(D3_GEO) }),
            loadScript(TOPOJSON),
            fetchJson(ATLAS)
        ])
        Promise.all([mapRequest, dataRequest]).then(function (results) {
            var data = results[1]
            globe = createGlobe(results[0][2], data ? data.countries : [])
        }).catch(function () {
            root.classList.add('visitor-globe--no-map')
        })
    }

    // fetch the map libraries only when the globe is about to be seen
    if ('IntersectionObserver' in window) {
        var observer = new IntersectionObserver(function (entries) {
            if (entries[0].isIntersecting) {
                observer.disconnect()
                start()
            }
        }, { rootMargin: '300px' })
        observer.observe(root)
    } else {
        start()
    }
})()
