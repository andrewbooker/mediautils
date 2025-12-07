function Tracks(container, disc) {
    var t = 0,
        audioControls = [],
        play = function(pos) {
            if (pos >= disc.trackList.length) {
                return function() {};
            }
            return function() {
                audioControls[pos].play();
                if (pos != audioControls.length) {
                    audioControls[pos + 1].load();
                }
            }
        };

    document.getElementsByTagName("title")[0].innerHTML = disc.title;
    document.getElementsByTagName("h1")[0].innerHTML = disc.title;

    while (t < disc.trackList.length) {
        container.appendChild((function() {
            var e = document.createElement("div"),
                tr = disc.trackList[t].split(".w")[0].split("_");
            e.setAttribute("style", "margin-top:0.6em");
            e.innerHTML = tr[tr.length - 1];
            return e;
        })());
        var audio = new Audio(disc.loc + "/" + disc.trackList[t]);
        audio.onended = play(t + 1);
        audio.controls = true;
        audioControls.push(audio);
        container.appendChild((function() {
            var e = document.createElement("div");
            e.appendChild(audio);
            return e;
        })());
        t += 1;
    }

    audioControls[0].load();
}
