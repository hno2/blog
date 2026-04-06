(function () {
              var gd = {{ GRAPH_DATA | safe }};
              var cur = "{{ article.slug }}";
              if (!gd.nodes.length) return;

              // Decode HTML entities
              var _ta = document.createElement('textarea');
              function decodeHtml(s) { _ta.innerHTML = s; return _ta.value; }

              function buildAdj(nodes, links) {
                var adj = {};
                nodes.forEach(function (n) { adj[n.id] = []; });
                links.forEach(function (l) {
                  if (adj[l.source]) adj[l.source].push(l.target);
                  if (adj[l.target]) adj[l.target].push(l.source);
                });
                return adj;
              }

              // Full adjacency list
              var fullAdj = buildAdj(gd.nodes, gd.links);

              // BFS neighbourhood
              var maxDepth = gd.depth || 1;
              var visibleIds = new Set([cur]);
              var queue = [[cur, 0]];
              while (queue.length) {
                var q = queue.shift(), qid = q[0], d = q[1];
                if (d < maxDepth) {
                  (fullAdj[qid] || []).forEach(function (nbr) {
                    if (!visibleIds.has(nbr)) {
                      visibleIds.add(nbr);
                      queue.push([nbr, d + 1]);
                    }
                  });
                }
              }
              var localNodes = gd.nodes.filter(function (n) { return visibleIds.has(n.id); });
              var localLinks = gd.links.filter(function (l) {
                return visibleIds.has(l.source) && visibleIds.has(l.target);
              });

              function byId(id) {
                for (var i = 0; i < gd.nodes.length; i++) {
                  if (gd.nodes[i].id === id) return gd.nodes[i];
                }
                return null;
              }

              function initMentioningPages() {
                var panel = document.getElementById('sidebar-mentioned-by-section');
                var list = document.getElementById('sidebar-mentioned-by-list');
                if (!panel || !list) return;

                var sourceIds = [];
                if (gd.incoming && Array.isArray(gd.incoming[cur])) {
                  sourceIds = gd.incoming[cur].slice();
                } else {
                  sourceIds = (fullAdj[cur] || []).slice();
                }

                var unique = [];
                var seen = {};
                for (var i = 0; i < sourceIds.length; i++) {
                  var sid = sourceIds[i];
                  if (!sid || sid === cur || seen[sid]) continue;
                  seen[sid] = true;
                  var node = byId(sid);
                  if (node && node.url) unique.push(node);
                }

                unique.sort(function (a, b) {
                  return (a.title || '').localeCompare((b.title || ''), undefined, { sensitivity: 'base' });
                });

                if (!unique.length) {
                  panel.hidden = true;
                  return;
                }

                for (var j = 0; j < unique.length; j++) {
                  var item = unique[j];
                  var li = document.createElement('li');
                  var a = document.createElement('a');
                  a.href = item.url;
                  a.textContent = decodeHtml(item.title || item.id);
                  li.appendChild(a);
                  list.appendChild(li);
                }
                panel.hidden = false;
              }

              function initTocHighlight() {
                var toc = document.getElementById('sidebar-toc-nav');
                if (!toc) return;

                var links = Array.prototype.slice.call(toc.querySelectorAll('a[href^="#"]'));
                if (!links.length) return;

                var entries = [];
                var topBranchById = {};

                function headingLevel(el) {
                  if (!el || !el.tagName) return 7;
                  var m = /^H([1-6])$/i.exec(el.tagName);
                  return m ? parseInt(m[1], 10) : 7;
                }

                for (var i = 0; i < links.length; i++) {
                  var href = links[i].getAttribute('href') || '';
                  var id = href.slice(1);
                  if (!id) continue;
                  var target = document.getElementById(decodeURIComponent(id));
                  if (!target) continue;
                  var li = links[i].closest('li');
                  if (!li) continue;
                  entries.push({
                    id: target.id,
                    link: links[i],
                    heading: target,
                    li: li,
                    level: headingLevel(target)
                  });
                }
                if (!entries.length) return;

                var baseLevel = 7;
                for (var e = 0; e < entries.length; e++) {
                  baseLevel = Math.min(baseLevel, entries[e].level);
                }

                var currentBranchId = null;
                var branchCount = 0;
                for (var k = 0; k < entries.length; k++) {
                  if (entries[k].level === baseLevel || !currentBranchId) {
                    currentBranchId = 'branch-' + branchCount;
                    branchCount += 1;
                    entries[k].li.dataset.branchId = currentBranchId;
                  }
                  topBranchById[entries[k].id] = currentBranchId;
                }

                var entryById = {};
                for (var m = 0; m < entries.length; m++) {
                  entryById[entries[m].id] = entries[m];
                }

                var anchorBiasId = null;
                var anchorBiasUntil = 0;

                function setAnchorBias(id) {
                  if (!id || !entryById[id]) return;
                  anchorBiasId = id;
                  anchorBiasUntil = Date.now() + 1400;
                }

                function clearClasses() {
                  var lis = toc.querySelectorAll('li');
                  for (var i = 0; i < lis.length; i++) {
                    lis[i].classList.remove('is-active-item', 'is-ancestor-item', 'is-current-branch');
                  }
                  var rails = toc.querySelectorAll('ul');
                  for (var r = 0; r < rails.length; r++) {
                    rails[r].classList.remove('is-active-rail');
                  }
                  for (var j = 0; j < entries.length; j++) {
                    entries[j].link.classList.remove('is-active');
                  }
                }

                function setActive(id) {
                  clearClasses();
                  var active = null;
                  for (var i = 0; i < entries.length; i++) {
                    if (entries[i].id === id) {
                      active = entries[i];
                      break;
                    }
                  }
                  if (!active) return;

                  active.link.classList.add('is-active');
                  active.li.classList.add('is-active-item');

                  var railNode = active.li;
                  while (railNode) {
                    var parentUl = railNode.parentElement;
                    if (parentUl && parentUl.tagName === 'UL') {
                      parentUl.classList.add('is-active-rail');
                    }
                    railNode = parentUl ? parentUl.closest('li') : null;
                  }

                  var ancestor = active.li.parentElement ? active.li.parentElement.closest('li') : null;
                  while (ancestor) {
                    ancestor.classList.add('is-ancestor-item');
                    ancestor = ancestor.parentElement ? ancestor.parentElement.closest('li') : null;
                  }

                  var branchId = topBranchById[id];
                  if (!branchId) return;
                  var branchNode = toc.querySelector('li[data-branch-id="' + branchId + '"]');
                  if (branchNode) {
                    branchNode.classList.add('is-current-branch');
                  }
                }

                function computeActiveId() {
                  if (anchorBiasId && Date.now() < anchorBiasUntil) {
                    var forced = entryById[anchorBiasId];
                    if (forced) {
                      var top = forced.heading.getBoundingClientRect().top;
                      if (top <= Math.round(window.innerHeight * 0.45)) {
                        return forced.id;
                      }
                    }
                  }

                  var y = window.scrollY + Math.round(window.innerHeight * 0.35);
                  if (entries[0].heading.offsetTop > y) {
                    return null;
                  }
                  var active = entries[0].id;
                  for (var i = 0; i < entries.length; i++) {
                    if (entries[i].heading.offsetTop <= y) {
                      active = entries[i].id;
                    } else {
                      break;
                    }
                  }
                  return active;
                }

                var ticking = false;
                function updateFromScroll() {
                  if (ticking) return;
                  ticking = true;
                  window.requestAnimationFrame(function () {
                    setActive(computeActiveId());
                    ticking = false;
                  });
                }

                window.addEventListener('scroll', updateFromScroll, { passive: true });
                window.addEventListener('resize', updateFromScroll);

                for (var l = 0; l < links.length; l++) {
                  links[l].addEventListener('click', function (ev) {
                    var href = ev.currentTarget.getAttribute('href') || '';
                    var id = href.charAt(0) === '#' ? href.slice(1) : '';
                    if (!id) return;
                    try {
                      id = decodeURIComponent(id);
                    } catch (_) {
                      // keep raw id if decode fails
                    }
                    setAnchorBias(id);
                    setActive(id);
                  });
                }

                window.addEventListener('hashchange', function () {
                  var raw = (window.location.hash || '').replace(/^#/, '');
                  if (!raw) return;
                  var id = raw;
                  try {
                    id = decodeURIComponent(raw);
                  } catch (_) {
                    // keep raw id if decode fails
                  }
                  setAnchorBias(id);
                  updateFromScroll();
                });

                if (window.location.hash) {
                  var initialId = window.location.hash.replace(/^#/, '');
                  try {
                    initialId = decodeURIComponent(initialId);
                  } catch (_) {
                    // keep raw id if decode fails
                  }
                  setAnchorBias(initialId);
                }

                updateFromScroll();
              }

              function initTocToggle() {
                var panel = document.getElementById('sidebar-toc-section');
                var toc = document.getElementById('sidebar-toc-nav');
                var button = document.getElementById('sidebar-toc-toggle-button');
                if (!panel || !toc || !button) return;

                var label = button.querySelector('.toc-toggle-label');
                var titleExpand = button.getAttribute('data-title-expand') || button.getAttribute('title') || '';
                var titleCollapse = button.getAttribute('data-title-collapse') || titleExpand;
                var labelExpand = button.getAttribute('data-label-expand') || (label ? label.textContent : '');
                var labelCollapse = button.getAttribute('data-label-collapse') || labelExpand;

                function setExpandedAll(expandedAll) {
                  panel.classList.toggle('is-expanded-all', expandedAll);
                  button.setAttribute('aria-pressed', expandedAll ? 'true' : 'false');
                  button.setAttribute('title', expandedAll ? titleCollapse : titleExpand);
                  if (label) {
                    label.textContent = expandedAll ? labelCollapse : labelExpand;
                  }
                }

                button.addEventListener('click', function () {
                  setExpandedAll(!panel.classList.contains('is-expanded-all'));
                });

                setExpandedAll(false);
              }

              // ── Graph factory ────────────────────────────────────────────
              function initGraph(cvs, rawNodes, rawLinks, warmup, maxH) {
                var c = cvs.getContext('2d');

                // local adjacency
                var ladj = buildAdj(rawNodes, rawLinks);

                // nodes with positions
                var nodes = rawNodes.map(function (n, i) {
                  var a = (i / rawNodes.length) * 2 * Math.PI;
                  var spread = 60 + Math.sqrt(rawNodes.length) * 15;
                  return { id: n.id, title: decodeHtml(n.title), url: n.url,
                           x: Math.cos(a) * spread, y: Math.sin(a) * spread,
                           vx: 0, vy: 0, degree: n.degree || 0 };
                });
                var nmap = Object.fromEntries(nodes.map(function (n) { return [n.id, n]; }));

                // radius scales with sqrt(degree); minimum raised for a larger default
                function nodeRadius(n) {
                  return n.id === cur ? 17 : Math.max(10, 9 + Math.sqrt(n.degree) * 3);
                }

                // force tick
                var K_REP = 9000, K_SPR = 0.04, REST = 110, K_CEN = 0.007;
                function tick() {
                  for (var i = 0; i < nodes.length; i++) {
                    for (var j = i + 1; j < nodes.length; j++) {
                      var dx = nodes[j].x - nodes[i].x || 0.01;
                      var dy = nodes[j].y - nodes[i].y || 0.01;
                      var d2 = dx*dx + dy*dy + 1;
                      var f = K_REP / d2;
                      nodes[i].vx -= f*dx; nodes[i].vy -= f*dy;
                      nodes[j].vx += f*dx; nodes[j].vy += f*dy;
                    }
                  }
                  rawLinks.forEach(function (l) {
                    var s = nmap[l.source], t = nmap[l.target];
                    if (!s || !t) return;
                    var dx = t.x-s.x, dy = t.y-s.y;
                    var d = Math.sqrt(dx*dx+dy*dy) + 0.01;
                    var f = (d - REST) * K_SPR;
                    s.vx += f*dx/d; s.vy += f*dy/d;
                    t.vx -= f*dx/d; t.vy -= f*dy/d;
                  });
                  nodes.forEach(function (n) {
                    n.vx -= n.x * K_CEN; n.vy -= n.y * K_CEN;
                    n.vx *= 0.65; n.vy *= 0.65;
                    n.x += n.vx; n.y += n.vy;
                  });
                }
                for (var _i = 0; _i < (warmup || 300); _i++) tick();

                // camera — all positions in CSS pixels
                var camX = 0, camY = 0, camZ = 1;
                function cW() { return parseInt(cvs.style.width) || cvs.width; }
                function cH() { return parseInt(cvs.style.height) || cvs.height; }
                function w2s(x, y) {
                  return [x*camZ + cW()/2 + camX, y*camZ + cH()/2 + camY];
                }
                function s2w(sx, sy) {
                  return [(sx - cW()/2 - camX)/camZ, (sy - cH()/2 - camY)/camZ];
                }
                function fitView() {
                  if (!nodes.length) return;
                  var x0=Infinity, x1=-Infinity, y0=Infinity, y1=-Infinity;
                  var maxTitleLen = 0;
                  nodes.forEach(function (n) {
                    x0=Math.min(x0,n.x); x1=Math.max(x1,n.x);
                    y0=Math.min(y0,n.y); y1=Math.max(y1,n.y);
                    maxTitleLen = Math.max(maxTitleLen, (n.title || '').length);
                  });
                  // Include extra room for node labels in the default fitted view.
                  var pad = Math.min(220, Math.max(95, 65 + maxTitleLen * 1.8));
                  camZ = Math.min(cW()/(x1-x0+pad*2), cH()/(y1-y0+pad*2)) * 0.9;
                  camX = -((x0+x1)/2)*camZ;
                  camY = -((y0+y1)/2)*camZ;
                }

                var hovId = null;

                // node colour palette – grayscale only
                function palette(n, hovAdj) {
                  var iC = n.id===cur, iH = n.id===hovId;
                  var iN = hovAdj && hovAdj.has(n.id);
                  if (iC) return '#111';
                  if (iH) return '#333';
                  if (iN) return '#555';
                  if (hovId) return '#ccc';
                  return '#888';
                }

                function render() {
                  c.clearRect(0, 0, cvs.width, cvs.height);
                  if (!cW() || !cH()) return;
                  var hovAdj = hovId ? new Set(ladj[hovId]||[]) : null;

                  // edges
                  rawLinks.forEach(function (l) {
                    var s = nmap[l.source], t = nmap[l.target];
                    if (!s||!t) return;
                    var sp = w2s(s.x,s.y), tp = w2s(t.x,t.y);
                    var hi = hovId && (l.source===hovId||l.target===hovId);
                    var isCE = l.source===cur||l.target===cur;
                    c.beginPath();
                    c.moveTo(sp[0],sp[1]); c.lineTo(tp[0],tp[1]);
                    c.strokeStyle = hi ? 'rgba(0,0,0,0.7)'
                                   : isCE ? 'rgba(0,0,0,0.25)'
                                   : 'rgba(0,0,0,0.12)';
                    c.lineWidth = hi ? 2.5 : isCE ? 1.5 : 1;
                    c.stroke();
                  });

                  // nodes
                  nodes.forEach(function (n) {
                    var p = w2s(n.x, n.y);
                    var baseR = nodeRadius(n);
                    var r = Math.max(baseR * Math.min(camZ, 1.5), 5);
                    var iC = n.id===cur, iH = n.id===hovId;
                    var isN = hovAdj && hovAdj.has(n.id);
                    var dimmed = hovId && !iC && !iH && !isN;

                    c.globalAlpha = dimmed ? 0.25 : 1;

                    // halo ring around selected / hovered node
                    if (iC || iH) {
                      var haloR = r + 5;
                      c.beginPath();
                      c.arc(p[0], p[1], haloR, 0, 2*Math.PI);
                      c.strokeStyle = iC ? 'rgba(0,0,0,0.25)' : 'rgba(0,0,0,0.18)';
                      c.lineWidth = 2;
                      c.stroke();
                    }

                    // flat fill, no border
                    c.beginPath();
                    c.arc(p[0], p[1], r, 0, 2*Math.PI);
                    c.fillStyle = palette(n, hovAdj);
                    c.fill();

                    c.globalAlpha = 1;

                    // wrapped label
                    var fs = Math.max(9, Math.round(11 * Math.min(camZ, 1.2)));
                    c.font = (iC||iH ? 'bold ' : '') + fs + 'px sans-serif';
                    c.fillStyle = dimmed ? 'rgba(0,0,0,0.2)' : iC ? '#000' : '#444';
                    c.textAlign = 'center';
                    c.textBaseline = 'alphabetic';
                    var maxW = Math.max(r * 2 + 20, 80);
                    var words = n.title.split(' ');
                    var lines = [], line = '';
                    for (var wi = 0; wi < words.length; wi++) {
                      var test = line ? line + ' ' + words[wi] : words[wi];
                      if (c.measureText(test).width > maxW && line) {
                        lines.push(line); line = words[wi];
                      } else { line = test; }
                    }
                    if (line) lines.push(line);
                    var ly = p[1] + r + 12;
                    for (var li = 0; li < lines.length; li++) {
                      c.fillText(lines[li], p[0], ly + li * (fs + 2));
                    }
                  });
                }

                // interaction helpers
                function cvs2xy(e) {
                  var rr = cvs.getBoundingClientRect();
                  var cx = e.touches ? e.touches[0].clientX : e.clientX;
                  var cy = e.touches ? e.touches[0].clientY : e.clientY;
                  return [cx-rr.left, cy-rr.top];
                }
                function findNode(mx, my) {
                  var w = s2w(mx, my);
                  for (var i = nodes.length-1; i >= 0; i--) {
                    var n = nodes[i];
                    var dx = n.x-w[0], dy = n.y-w[1];
                    if (Math.sqrt(dx*dx+dy*dy) <= nodeRadius(n)/camZ + 6) return n.id;
                  }
                  return null;
                }

                var isPan=false, lastM=[0,0], clickStart=[0,0];

                function onMove(e) {
                  var p = cvs2xy(e);
                  var found = findNode(p[0],p[1]);
                  var needsRender = false;
                  if (found !== hovId) {
                    hovId=found; cvs.style.cursor=found?'pointer':'default';
                    needsRender = true;
                  }
                  if (isPan) {
                    camX+=e.clientX-lastM[0]; camY+=e.clientY-lastM[1];
                    lastM=[e.clientX,e.clientY];
                    needsRender = true;
                  }
                  if (needsRender) render();
                }
                function onLeave() { hovId=null; isPan=false; render(); }
                function onDown(e) { clickStart=[e.clientX,e.clientY]; lastM=[e.clientX,e.clientY]; isPan=true; e.preventDefault(); }
                function onUp() { isPan=false; }
                function onClick(e) {
                  var mv = Math.abs(e.clientX-clickStart[0])+Math.abs(e.clientY-clickStart[1]);
                  var n = mv<5 && hovId && nmap[hovId];
                  if (n && n.url) window.location.href=n.url;
                }
                function onWheel(e) {
                  e.preventDefault();
                  var p=cvs2xy(e), w=s2w(p[0],p[1]);

                  // Normalize wheel delta for consistent zoom across mouse/trackpad.
                  var delta = Number.isFinite(e.deltaY) ? e.deltaY : 0;
                  delta *= e.deltaMode === 1 ? 16 : e.deltaMode === 2 ? 100 : 1;

                  // Cap single-event impact to avoid sudden jumps on trackpads/pinch.
                  delta = Math.max(-60, Math.min(60, delta));
                  if (Math.abs(delta) < 0.01) return;

                  // Use exponential scale for smooth, reversible zoom in both directions.
                  var zoom = Math.exp(-delta * 0.0012);
                  camZ = Math.max(0.1, Math.min(camZ * zoom, 20));

                  // Keep world point under cursor fixed (CSS pixel space).
                  camX = p[0] - cW()/2 - w[0] * camZ;
                  camY = p[1] - cH()/2 - w[1] * camZ;
                  render();
                }
                function onDbl() { fitView(); render(); }

                var listeners = [
                  [cvs, 'mousemove', onMove],
                  [cvs, 'mouseleave', onLeave],
                  [cvs, 'mousedown', onDown],
                  [cvs, 'click', onClick],
                  [cvs, 'wheel', onWheel, { passive: false }],
                  [cvs, 'dblclick', onDbl],
                  [window, 'mouseup', onUp]
                ];
                listeners.forEach(function (x) { x[0].addEventListener(x[1], x[2], x[3]); });

                function resize() {
                  var p = cvs.parentElement;
                  var dpr = window.devicePixelRatio || 1;
                  var cssW = p.offsetWidth;
                  var cssH = maxH
                    ? Math.round(window.innerHeight * maxH)
                    : Math.min(Math.round(window.innerHeight * 0.5), 360);
                  cvs.width  = Math.round(cssW * dpr);
                  cvs.height = Math.round(cssH * dpr);
                  cvs.style.width  = cssW + 'px';
                  cvs.style.height = cssH + 'px';
                  c.setTransform(dpr, 0, 0, dpr, 0, 0);
                  fitView(); render();
                }
                resize();
                var ro = new ResizeObserver(resize);
                ro.observe(cvs.parentElement);

                return {
                  cleanup: function () {
                    listeners.forEach(function (x) { x[0].removeEventListener(x[1], x[2], x[3]); });
                    ro.disconnect();
                  }
                };
              }
              // ─────────────────────────────────────────────────────────────

              // Sidebar: neighbourhood graph
              initGraph(
                document.getElementById('sidebar-graph-canvas'),
                localNodes, localLinks, 300, null
              );

              // Pop-out: full graph
              var overlayG = null;
              var overlay = document.getElementById('sidebar-graph-overlay');
              function closeOverlay() { overlay.style.display = 'none'; }
              document.getElementById('sidebar-graph-expand-button').addEventListener('click', function () {
                overlay.style.display = 'flex';
                if (!overlayG) {
                  overlayG = initGraph(
                    document.getElementById('sidebar-graph-overlay-canvas'),
                    gd.nodes, gd.links, 500, 0.85
                  );
                }
              });
              document.getElementById('sidebar-graph-overlay-close').addEventListener('click', closeOverlay);
              overlay.addEventListener('click', function (e) {
                if (e.target === overlay) closeOverlay();
              });
              document.addEventListener('keydown', function (e) {
                if (e.key === 'Escape') closeOverlay();
              });

              initMentioningPages();
              initTocToggle();
              initTocHighlight();
            })();
