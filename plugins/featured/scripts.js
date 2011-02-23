var autoSlide = true;
var autoSlideSecs = 10;

var proj = 0;
var interval = null;

function textSlideIn (proj) {
    $('ul.featured_text').children ('li:eq(' + proj + ')').animate ({ right: "-1px" }, 700);
}
function textSlideOut (proj) {
    $('ul.featured_text').children ('li:eq(' + proj + ')').animate ({ right: "-50%" }, 700);
}
function photoFadeIn (proj) {
    $('ul.featured_photo').children ('li:eq(' + proj + ')').fadeIn (700);
}
function photoFadeOut (proj) {
    $('ul.featured_photo').children ('li:eq(' + proj + ')').fadeOut (700);
}
function photoPutBehind (proj) {
    $('ul.featured_photo').children ('li:eq(' + proj + ')').css ('z-index', 0);
}
function nextSlide () {
    $('ul.featured_photo').children ('li:eq(' + proj + ')').css ("z-index", 2);
    setTimeout ('photoFadeOut(' + proj + ')', 1000);
    setTimeout ('photoPutBehind(' + proj + ')', 1500);
    textSlideOut (proj);
    proj++;
    var i = $('ul.featured_text li').size () - 1;
    if (proj>i) proj = 0;
    setTimeout ('photoFadeIn(' + proj + ')', 1000);		
    setTimeout ('textSlideIn(' + proj + ')', 1500);
}

$(function () {
    if (autoSlide) interval = setInterval ('nextSlide()', autoSlideSecs * 1000);
    jQuery('.next').click (function () {
        clearInterval (interval);
        nextSlide ();
        if (autoSlide) interval = setInterval ('nextSlide()', autoSlideSecs * 1000);
        return false;
    });
});

