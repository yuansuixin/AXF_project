$(function () {

    initTopSwiper();
    initswiperMenu();


})
//首页的轮播图
function initTopSwiper() {
    var swiper = Swiper("#topSwiper",{
        pagination:'.swiper-pagination',
        autoplay:2000,
    })
}


//mustbuy多个显示
function initswiperMenu() {
var swiper = new Swiper('#swiperMenu', {
      slidesPerView: 3,
      // spaceBetween: 30,
      paginationClickable: true,
      spaceBetween: 2,
      loop: false,
    });
}

