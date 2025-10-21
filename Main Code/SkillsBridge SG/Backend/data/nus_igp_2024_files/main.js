//************ Header/footer/mobile sidebar style guide **************/

//move web content to left when click sidebarcount

function openSidebar(e) {
    e.stopPropagation();

    $('.nus-wrapbody').addClass('show-sidebar');
    $('.nus-wrapbody').css('width', '100vw');
    $('.nus-sidemenu').addClass('show');
    $('.nus-openoverlay-button').attr('aria-expanded', 'true');

    if ($('.nus-overlay-box').css('display') == 'none') {
        $('.nus-overlay-box').css('display', 'block');
    }
    $('html').css({ overflow: 'hidden', height: '100%' });
    $('body').bind('touchmove', false);
}

function closeSidebar() {
    $('.nus-wrapbody').removeClass('show-sidebar');
    $('.nus-wrapbody').css('width', '100%');
    $('.nus-sidemenu').removeClass('show');
    $('.nus-openoverlay-button').attr('aria-expanded', 'false');
    if ($('.nus-overlay-box').css('display') == 'block') {
        $('.nus-overlay-box').css('display', 'none');
        $('html').css({ overflow: 'auto', height: 'auto' });
        $('body').bind('touchmove', true);
        $('.nus-openoverlay-button').attr('aria-expanded', 'false');
    }
}

$(document).on('click', '.nus-wrapbody', closeSidebar);
$(document).on('click', '.nus-closeoverlay-button', closeSidebar);
$(document).on('click', '.nus-openoverlay-button', openSidebar)

//when resize browser sidebar menu close
function overlay_action() {
    if ($(window).width() > 992) {
        closeSidebar();
    }
}
$(window).on('load resize orientationchange', overlay_action);


$('.mobile-right-menu .nav-item button').click(function () {
    $(this).attr('aria-expanded', 'true');
});

//For mouse hover on menu list for accessibility screen reader

$('.dropdown-item').mouseover(function () {
    $(this).attr('aria-expanded', 'true');
});

$('.dropdown-item').mouseleave(function () {
    $(this).attr('aria-expanded', 'false');
});

$('.nav .nav-item.dropdown .dropdown-menu').hover(function () {
    $(this).removeClass('d-none');
})

// Remove hover class when user click the item
$('.nav .nav-item .dropdown-menu .dropdown-item').on('click', function () {
    $(this).parent().parent().addClass('d-none');
})

//For mobile selected active blue
$('.sidebar .nav .nav-item a').each(function () {

    $(this).removeClass('active');

    if (location.href == this.href) {
        $(this).parents('.nav-item').find('a.nav-link').addClass('active');
        $(this).parents('.nav-item').find('ul li a').removeClass('active');
    }
});

// search bar slide toggle
$('.nus-searchpanel').hide();
$('.search-slide').click(function () {
    $('.nus-searchpanel').slideToggle('fast');
});

var active = false;

$('.search-slide').on('click', function () {
    if (active == false) {
        $('.fa-search').css("color", "#EF7C00");
        active = true;
        $('.search-slide').attr('aria-expanded', 'true');
    } else {
        $('.fa-search').css('color', '#000');
        active = false;
        $('.search-slide').attr('aria-expanded', 'false');
    }
});


//************ Header/footer/mobile sidebar style guide **************/


// homepage

var swiper = new Swiper(".homepage-swiper", {
    loop: true,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },

    pagination: {
        el: ".swiper-pagination",
        clickable: true
    },
});

$(window).on('resize orientationchange load', function () {
    if ((window).innerWidth > 768) {

        // set the all columns to the height of the tallest column by using a function
        var equalHeight = function () {

            $('.nus-rating').each(function () {
                const columns = $(this).children().map(function () { return $(this).children() }).toArray();
                if (!columns.length) return;

                const rowCount = columns[0].length;

                for (let i = 0; i < rowCount; i++) {
                    let maxHeight = 0;
                    for (let j = 0; j < columns.length; j++) {
                        maxHeight = Math.max(maxHeight, $(columns[j][i]).height());
                    }
                    for (let j = 0; j < columns.length; j++) {
                        $(columns[j][i]).css('height', maxHeight + 'px')
                    }
                }
            })
        };
        //  equal height set on page load
        equalHeight();
    }
});

$(window).on('resize orientationchange load', function () {
    if ((window).innerWidth < 768) {
        $('.nus-experience-section .column h6, .nus-experience-section .column p').removeAttr("style");
    }
});


// $(window).on('scroll', function() {
//   const nusRatingTop = Math.max(0, $('.nus-rating').offset().top - $(window).height());
//   if ($(window).scrollTop() > nusRatingTop) {
//     $('.count:not(.played)').each(function () {
//       $(this).addClass('played')
//       $(this).prop('Counter',0).animate({
//           Counter: $(this).text()
//       }, {
//           duration: 2500,
//           easing: 'swing',
//           step: function (now) {
//               $(this).text(Math.ceil(now));
//           },
//       });
//     });
//   }
// })


$(window).on('scroll', function () {

    if ($('.nus-rating') && $('.nus-rating').offset() != null) {
        const nusRatingTop = Math.max(0, $('.nus-rating').offset().top - $(window).height());

        if ($(window).scrollTop() > nusRatingTop) {
            $('.count:not(.played)').each(function () {
                var originalText = $(this).text();
                var originalNumber = extractNumberFromString(originalText)

                $(this).addClass('played')
                $(this).prop('Counter', 0).animate({
                    Counter: originalNumber
                }, {
                    duration: 2500,
                    easing: 'swing',
                    step: function (now) {
                        if (originalNumber) {
                            var newText = replaceNumberInText(originalText, originalNumber, Math.ceil(now));
                            $(this).text(newText);
                        }
                    },
                });
            });
        }
    }

})


function replaceNumberInText(originalText, originalNumber, newNumber) {
    const escapedOriginalNumber = originalNumber.toString().replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

    return originalText.replace(new RegExp(escapedOriginalNumber, 'g'), newNumber);
}

function extractNumberFromString(text) {
    let matches = text.match(/(\d+(\.\d+)?)/g);

    return matches ? matches[0] : null;
}


var swiper = new Swiper('.announcements-swiper', {

    // Navigation arrows
    navigation: {
        nextEl: '.announcementsswiper-button-next',
        prevEl: '.announcementsswiper-button-prev',
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true
    },

    // Responsive breakpoints
    breakpoints: {
        320: {
            slidesPerView: 1,
            slidesPerGroup: 1,
            spaceBetween: 30
        },
        768: {
            slidesPerView: 2,
            slidesPerGroup: 2,
            spaceBetween: 30
        },
        1200: {
            slidesPerView: 3,
            slidesPerGroup: 3,
            spaceBetween: 30
        }
    }
});

$(window).on('resize orientationchange load', function () {
    // set the all columns to the height of the tallest column by using a function
    var equalHeight = function () {
        //  the height of each column is reset to default calculated by browser
        $('.swiper-slide .announcements-swiper__detail p').css('height', 'auto');
        var maxHeight = 0;
        // get the maximum height
        $('.swiper-slide .announcements-swiper__detail p').each(function () {
            if ($(this).height() > maxHeight) {
                maxHeight = $(this).height();
            }
        });
        // the maximum height is set to each height of column
        $('.swiper-slide .announcements-swiper__detail p').css('height', maxHeight);
    };
    //  equal height set on page load
    equalHeight();
});

var swiper = new Swiper('.events-swiper', {

    // Navigation arrows
    navigation: {
        prevEl: '.eventsswiper-button-prev',
        nextEl: '.eventsswiper-button-next',
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true
    },

    // Responsive breakpoints
    breakpoints: {
        320: {
            slidesPerView: 1,
            slidesPerGroup: 1, /* The answer to your Q */
            spaceBetween: 30
        },
        768: {
            slidesPerView: 2,
            slidesPerGroup: 2, /* The answer to your Q */
            spaceBetween: 30
        },

    }
});

$(window).on('resize orientationchange load', function () {

    // set the all columns to the height of the tallest column by using a function
    var equalHeight = function () {
        //  the height of each column is reset to default calculated by browser
        $('.academic-section .academic-section__right ').css('height', 'auto');
        var maxHeight = 0;
        // get the maximum height
        $('.academic-section .academic-section__right ').each(function () {
            if ($(this).height() > maxHeight) {
                maxHeight = $(this).height();
            }
        });
        // the maximum height is set to each height of column
        $('.academic-section').css('height', maxHeight);
    };
    //  equal height set on page load
    equalHeight();

});

$(window).on('resize orientationchange load', function () {
    if ((window).innerWidth < 992) {

        $('.academic-section').removeAttr('style');
    }
});


$(window).on('resize orientationchange load', function () {
    // set the all columns to the height of the tallest column by using a function
    var equalHeight = function () {
        //  the height of each column is reset to default calculated by browser
        $('.academic-section .academic-section__right  .academic-detail-box p').css('height', 'auto');
        var maxHeight = 0;
        // get the maximum height
        $('.academic-section .academic-section__right  .academic-detail-box p').each(function () {
            if ($(this).height() > maxHeight) {
                maxHeight = $(this).height();
            }
        });
        // the maximum height is set to each height of column
        $('.academic-section .academic-section__right  .academic-detail-box p').css('height', maxHeight);
    };
    //  equal height set on page load
    equalHeight();
});

$(window).on('resize orientationchange load', function () {
    // set the all columns to the height of the tallest column by using a function
    var equalHeight = function () {
        //  the height of each column is reset to default calculated by browser
        $('.admissions-section .admissions-section__detail p').css('height', 'auto');
        var maxHeight = 0;
        // get the maximum height
        $('.admissions-section .admissions-section__detail p').each(function () {
            if ($(this).height() > maxHeight) {
                maxHeight = $(this).height();
            }
        });
        // the maximum height is set to each height of column
        $('.admissions-section .admissions-section__detail p').css('height', maxHeight);
    };
    //  equal height set on page load
    equalHeight();
});


//applynus

function updateDot() {
    const index = $(this).index() + 1
    const totalDot = $('.dot').length
    $(`.dot:not(:nth-child(-n+${index}))`).removeAttr('style')
    $(`.dot:nth-child(-n+${index})`).css({ 'border-color': '#EF7C00', 'background-color': '#003062', 'box-shadow': '0px 3px 6px #000000B5' });
    $(`.dot:nth-child(-n+${index})`).find('.progress-detail, .progress-detail a.link').css({ 'color': '#333333', 'border-color': '#EF7C00', 'font-weight': 'bold' });
    $(`.dot:nth-child(-n+${index})`).find('.progress-detail a.link').css({ 'color': '#e20000', 'font-weight': 'bold' });

    $(`.dot:not(:nth-child(-n+${index})) .progress-detail`).css({ 'color': '#CECBCB', 'border-color': '#CECBCB', 'font-weight': 'normal' });
    $(`.dot:not(:nth-child(-n+${index})) .progress-detail a.link`).css({ 'color': '#CECBCB', 'font-weight': 'normal' });
    const percentage = index == totalDot ? 100 : (index * 2 - 1) / (totalDot * 2) * 100
    $('.inside').animate({ 'width': `${percentage}%` }, 500);
}

$('.dot').click(updateDot);

$('.dot.active').each(updateDot)

if (($('.dot').length) <= 5) {
    $('.arrow-scroll').addClass('d-none');
}
else {
    $('.arrow-scroll').addClass('d-flex');
}

$(document).ready(function () {
    //Default Action

    $(".tabmain_content").hide(); //Hide all content
    $(".dot:first").addClass("active").show(); //Activate first tab
    $(".tabmain_content:first").show(); //Show first tab content

    //On Click Event

    $(this).find(".progress-detail .link").click(function () {
        var link = $(this).attr('href');
        console.log(link);
        window.location.href = link;
    });

    $(".dot").click(function () {

        $(".dot").removeClass("active"); //Remove any "active" class
        $(this).addClass("active"); //Add "active" class to selected tab
        $(".tabmain_content").hide(); //Hide all tab content
        var activeTab = $(this).attr("id"); //Find the rel attribute value to identify the active tab + content
        $(activeTab).fadeIn(); //Fade in the active content
    });
});

const mouseWheel = document.querySelector('.box-scroll');

if (mouseWheel) {
    mouseWheel.addEventListener('wheel', function (e) {
        const race = 15; // How many pixels to scroll

        if (e.deltaY > 0) // Scroll right
            mouseWheel.scrollLeft += race;
        else // Scroll left
            mouseWheel.scrollLeft -= race;
        e.preventDefault();
    });
}

const slider = document.querySelector('.box-scroll');
let isDown = false;
let startX;
let scrollLeft;

if (slider) {

    slider.addEventListener('mousedown', (e) => {
        isDown = true;
        slider.classList.add('active');
        startX = e.pageX;
        scrollLeft = slider.scrollLeft;
    });

    slider.addEventListener('mouseleave', () => {
        isDown = false;
        slider.classList.remove('active');
    });

    slider.addEventListener('mouseup', () => {
        isDown = false;
        slider.classList.remove('active');
    });

    slider.addEventListener('mousemove', (e) => {
        if (!isDown) return;  // stop the fn from running
        e.preventDefault();
        slider.scrollLeft = scrollLeft - (e.pageX - startX) * 2
    });

}

var box = $(".box-scroll"), x;
$(".arrow").click(function () {
    if ($(this).hasClass("arrow-right")) {
        x = ((box.width() / 2)) + box.scrollLeft();
        box.animate({
            scrollLeft: x,
        })
    } else {
        x = ((box.width() / 2)) - box.scrollLeft();
        box.animate({
            scrollLeft: -x,
        })
    }
});

$(".expand").click(function () {

    if ($(this).data("closedAll")) {
        $(".accdion.collapse").collapse("show");
    }
    else {
        $(".accdion.collapse").collapse("hide");
    }

    $(this).toggleClass("active");

    // save last state
    $(this).data("closedAll", !$(this).data("closedAll"));
});

// init with all closed
$(".expand").data("closedAll", true);


$(window).on('resize orientationchange load', function () {
    // set the all columns to the height of the tallest column by using a function
    var equalHeight = function () {
        //  the height of each column is reset to default calculated by browser
        $('.card .card-wrap p, .card .card-wrap .card-body p').css('height', 'auto');
        var maxHeight = 0;
        // get the maximum height
        $('.card .card-wrap p, .card .card-wrap .card-body p').each(function () {
            if ($(this).height() > maxHeight) {
                maxHeight = $(this).height();
            }
        });
        // the maximum height is set to each height of column
        $('.card .card-wrap p, .card .card-wrap .card-body p').css('height', maxHeight);
    };
    //  equal height set on page load
    equalHeight();
});


$(window).on('resize orientationchange load', function () {
    // set the all columns to the height of the tallest column by using a function
    var equalHeight = function () {
        //  the height of each column is reset to default calculated by browser
        $('.card .card-wrap .card-body p').css('height', 'auto');
        var maxHeight = 0;
        // get the maximum height
        $('.card .card-wrap .card-body p').each(function () {
            if ($(this).height() > maxHeight) {
                maxHeight = $(this).height();
            }
        });
        // the maximum height is set to each height of column
        $('.card .card-wrap .card-body p').css('height', maxHeight);
    };
    //  equal height set on page load
    equalHeight();
});


//undergrauate

function handleMouseenterNUSCard() {

    const slide = $(this).find('.info-slide');
    const $descEl = $(this).find('.info-slide-desc');
    const $pointerEl = $(this).find('.oam-academic-card-learn-more-btn .pointer');
    const $pointerDownEl = $(this).find('.oam-academic-card-learn-more-btn .pointer-down');
    const learnMoreButton = $(this).find('.oam-academic-card-learn-more-btn');
    const arrowColor = $pointerDownEl.parent().data("arrow-color");

    learnMoreButton.addClass(learnMoreButton.data("btn-color"));

    slide.addClass('selected')
    $(this).parents('.nus-card-box').find('.info-slide:not(.selected)').addClass('unselected');
    $descEl.fadeIn();
    $descEl.css('box-shadow', '0px 3px 6px rgba(0,0,0,0.3)');
    const marginBottom = $descEl.outerHeight() + 50 + 'px';
    $pointerEl.fadeIn();
    
    if ($(window).outerWidth() >= 992) {
        $(this).parents('.nus-card-box').css('margin-bottom', marginBottom);
    } else {
        $(this).css('margin-bottom', marginBottom)
    }

    $pointerDownEl.fadeIn();
    $pointerDownEl.css("background", "linear-gradient(-45deg," + arrowColor + " 50%,transparent 50%)");
    if ($(window).outerWidth() >= 992) {
        $(this).parents('.nus-card-box').css('margin-bottom', marginBottom);
    } else {
        $(this).css('margin-bottom', marginBottom)
    }
}

function handleMouseoutNUSCard() {
    const $slide = $(this).find('.info-slide');
    const $pointerEl = $(this).find('.pointer');
    const $pointerDownEl = $(this).find('.oam-academic-card-learn-more-btn .pointer-down');
    const learnMoreButton = $(this).find('.oam-academic-card-learn-more-btn');

    $slide.removeClass('selected')
    $(this).parents('.nus-card-box').find('.info-slide').removeClass('unselected');
    $(this).parents('.nus-card-box').find('.info-slide-desc').fadeOut('fast');
    learnMoreButton.removeClass(learnMoreButton.data("btn-color"));

    $pointerEl.fadeOut('fast');
    if ($(window).outerWidth() >= 992) {
        $pointerEl.css('left', '');
        $pointerEl.css('top', '');
        $(this).parents('.nus-card-box').css('margin-bottom', '');
    } else {
        $(this).css('margin-bottom', '')
    }

    $pointerDownEl.fadeOut('fast');
    if ($(window).outerWidth() >= 992) {
        $pointerDownEl.css('left', '');
        $pointerDownEl.css('top', '');
        $(this).parents('.nus-card-box').css('margin-bottom', '');
    } else {
        $(this).css('margin-bottom', '')
    }
}

$('.nus-card').on('mouseenter', handleMouseenterNUSCard);
$('.nus-card').on('mouseleave', handleMouseoutNUSCard);

$(window).on('resize orientationchange load', function () {
    // set the all columns to the height of the tallest column by using a function
    var equalHeight = function () {
        //  the height of each column is reset to default calculated by browser
        $('.oam-academic-card-media ').css('height', 'auto');
        var maxHeight = 0;
        // get the maximum height
        $('.oam-academic-card-media ').each(function () {
            if ($(this).height() > maxHeight) {
                maxHeight = $(this).height();
            }
        });
        // the maximum height is set to each height of column
        $('.oam-academic-card-media ').css('height', maxHeight);
    };
    //  equal height set on page load
    equalHeight();
});

$(window).on('resize orientationchange load', function () {
    if ((window).innerWidth < 992) {
        $('.oam-academic-card-media').removeAttr('style');
    }
});

$('.anchor-menu').each(function () {
    const $swiper = $(this).find('.swiper');
    const $scrollbar = $(this).find('.anchor-menu-scrollbar');
    const $left = $(this).find('.anchor-menu-left');
    const $right = $(this).find('.anchor-menu-right');
    if ($swiper.length) {
        new Swiper($swiper.get(0), {
            spaceBetween: 0,
            slidesPerView: 'auto',
            centerInsufficientSlides: true,
            scrollbar: {
                el: $scrollbar.get(0),
                draggable: true
            },
            navigation: {
                nextEl: $right.get(0),
                prevEl: $left.get(0),
            },
        });
    }
})

$(".detail-content").hide();
$(".swiper-wrapper a.swiper-slide:first").addClass("active").show();
$(".detail-content:first").show();

$(".swiper-wrapper a.swiper-slide").click(function () {
    $(".swiper-wrapper a.swiper-slide").removeClass("active");
    $(this).addClass("active");
    $(".detail-content").hide();
    var activeTab = $(this).attr("href");
    $(activeTab).fadeIn();
    return false;
});


$(".course-listing-wrapper").hide();
$(".course-selection-tab ul.course-selection-cat a:first").addClass("active").show();
$(".course-listing-wrapper:first").show();

$(".course-selection-tab ul.course-selection-cat a").click(function () {
    $(".course-selection-tab ul.course-selection-cat a").removeClass("active");
    $(this).addClass("active");
    $(".course-listing-wrapper").hide();
    var activeTab = $(this).attr("href");
    $(activeTab).fadeIn();
    return false;
});


$(window).on('resize orientationchange load', function () {
    if ($(window).outerWidth() > 992) {
        let highestWidth = 0; 
        $(".nus-pathway-section .detail-content .nus-pathway-box .nus-card-box").each(function () {
            const rowWidth = $(this).outerWidth();
            const cardWidth = $(this).find('.col-lg-3 > .nus-card').outerWidth();
            const cardCount = $(this).find('.col-lg-3').length;
            const gutterWidth = (rowWidth - 4 * cardWidth) / 8;
            const totalWidth = (cardCount - 1) * 2 * gutterWidth + cardCount * cardWidth
            if(totalWidth > highestWidth)
            {
                highestWidth = totalWidth;
            }
            $(this).find('.info-slide-desc').css('width', (totalWidth !=0 ? totalWidth : highestWidth) + 'px')
        });
    } else {
        $(".nus-pathway-section .detail-content .nus-pathway-box .nus-card-box").find('.col-lg-3 .info-slide-desc').css('width', '100%');
    }
});


//why nus

var swiper = new Swiper('.studentSwiper', {
    autoplay: {
        delay: 5000,
    },
    spaceBetween: 15,
    initialSlide: 1,
    slideToClickedSlide: true,
    pagination: {
        el: '.swiper-pagination',
        clickable: true
    },
    centeredSlides: true,

});

$(window).on('load orientationchange resize', function () {

    $('.nus-student-carousel').each(function () {
        let height = 0;
        $(this).find('.nus-student-carousel-box').css('height', '');
        $(this).find('.nus-student-carousel-box').each(function () {
            height = Math.max(height, $(this).outerHeight());
        });
        $(this).find('.nus-student-carousel-box').css('height', height + 'px');
    })
});

const myModal = document.querySelector('#mymodal');

if (myModal) {

    myModal.addEventListener('show.bs.modal', function (event) {

        const popupcontent = event.relatedTarget;
        const profileimage = popupcontent.getAttribute('data-bs-image');
        const profilename = popupcontent.getAttribute('data-bs-name');
        const profilecourse = popupcontent.getAttribute('data-bs-course');
        const profilemajor = popupcontent.getAttribute('data-bs-major');
        const profilecontent = popupcontent.getAttribute('data-bs-modalcontent');
        $('#my_image').attr('src', profileimage);
        myModal.querySelector('.name').innerHTML = profilename;
        myModal.querySelector('.course').innerHTML = profilecourse;
        myModal.querySelector('.major').innerHTML = profilemajor;
        myModal.querySelector('.content').innerHTML = profilecontent;

    });

}

$(window).on('resize orientationchange load', function () {
    // set the all columns to the height of the tallest column by using a function
    var equalHeight = function () {
        //  the height of each column is reset to default calculated by browser
        $('.profile-detail .course, .profile-detail .major').css('height', 'auto');
        var maxHeight = 0;
        // get the maximum height
        $('.profile-detail .course, .profile-detail .major').each(function () {
            if ($(this).outerHeight() > maxHeight) {
                maxHeight = $(this).outerHeight();
            }
        });
        // the maximum height is set to each height of column
        $('.profile-detail .course, .profile-detail .major').css('height', maxHeight);
    };
    //  equal height set on page load
    equalHeight();
});

$(".accordion-button b").click(function () {
    var dataUrl = $(this).data("url").replace("~", "");
    if (dataUrl && dataUrl != "") {
        if (!dataUrl.includes("/oam/")) {
            dataUrl = "/oam" + dataUrl;
        }
        window.location.href = dataUrl;
    }
})

$(".sidenav .nav-item .parent-title").click(function () {
    var dataUrl = $(this).data("url").replace("~", "");
    if (dataUrl && dataUrl != "") {
        if (!dataUrl.includes("/oam/") && $(this).text() != "Home") {
            dataUrl = "/oam" + dataUrl;
        }
        window.location.href = dataUrl;
    }
})

$(".sidenav .nav-item .submenu .child-title").click(function () {
    var dataUrl = $(this).data("url").replace("~", "");
    if (dataUrl && dataUrl != "") {
        if (!dataUrl.includes("/oam/")) {
            dataUrl = "/oam" + dataUrl;
        }
        window.location.href = dataUrl;
    }
})

$(".accordion-section .accordion-button").each(function (i, e) {
    $(e).click(function () {
        var parent = $(e).closest(".accordion-section");
        var expandButton = parent.find(".expand");
        var expandAccordionNumber = parent.find(".accordion-button[aria-expanded='true']").length;
        var collapseAccordionNumber = parent.find(".accordion-button[aria-expanded='false']").length;
        var totalAccordion = parent.find(".accordion-button").length;

        if (expandAccordionNumber == totalAccordion) {
            expandButton.removeClass("active");
            expandButton.data("closedAll", false);
        }

        if (collapseAccordionNumber == totalAccordion) {
            expandButton.addClass("active");
            expandButton.data("closedAll", true);
        }
    })
})