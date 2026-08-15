<template>
  <section class="hero-slider">
    <div class="container hero-container">
      <!-- Content -->
      <div class="hero-content">
        <span class="eyebrow">
          {{ currentSlide.label }}
        </span>
        <h1>
          {{ currentSlide.title }}
        </h1>
        <p>
          {{ currentSlide.description }}
        </p>
        <div class="hero-actions">
          <router-link
            :to="currentSlide.primaryLink"
            class="btn btn-accent"
          >
            {{ currentSlide.primaryText }}
          </router-link>
          <router-link
            :to="currentSlide.secondaryLink"
            class="btn btn-outline"
          >
            {{ currentSlide.secondaryText }}
          </router-link>
        </div>
      </div>
      <!-- Image -->
      <div class="hero-image">
        <div class="image-placeholder">
          🐫
        </div>
      </div>
    </div>
    <!-- Controls -->
    <button
      class="slider-prev"
      @click="previous"
    >
      ‹
    </button>
    <button
      class="slider-next"
      @click="next"
    >
      ›
    </button>
    <div class="slider-dots">
      <button
        v-for="(item,index) in slides"
        :key="index"
        :class="{active:index===currentIndex}"
        @click="goTo(index)"
      >
      </button>
    </div>
  </section>
</template>



<script>

export default {


name:"HeroSlider",


data(){

return{


currentIndex:0,


timer:null,


slides:[


{
label:"فروشگاه یاشیل آرت",

title:"هر خرید، آغاز یک مسیر مطمئن",

description:
"از محصولات منتخب تا تجربه خرید آسان؛ یاشیل آرت همراه شماست.",

primaryText:"مشاهده محصولات",

primaryLink:"/products",

secondaryText:"پیشنهاد ویژه",

secondaryLink:"/products?featured=1"

},



{
label:"پیشنهاد ویژه",

title:"بهترین محصولات با بهترین قیمت",

description:
"تخفیف‌های ویژه را از دست ندهید.",

primaryText:"مشاهده تخفیف‌ها",

primaryLink:"/products?has_discount=1",

secondaryText:"محصولات جدید",

secondaryLink:"/products"

}



]


}

},


computed:{


currentSlide(){

return this.slides[this.currentIndex];

}


},



mounted(){

this.startSlider();

},



beforeDestroy(){

clearInterval(this.timer);

},



methods:{


next(){

this.currentIndex =
(this.currentIndex+1)%this.slides.length;

},



previous(){

this.currentIndex =
(this.currentIndex-1+this.slides.length)
%this.slides.length;

},



goTo(index){

this.currentIndex=index;

},



startSlider(){

this.timer=setInterval(()=>{

this.next();

},5000);


}



}


};

</script>



<style scoped>


.hero-slider{

position:relative;

width:100%;

overflow:hidden;

background:var(--color-primary);

color:white;

}



.hero-container{
    min-height:330px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:40px;
    padding-top:20px;
    padding-bottom:20px;
}



.hero-content{


max-width:560px;


}



.hero-content h1{
    font-size:2.2rem;
    line-height:1.35;
    margin:15px 0;
    color:white;
}



.hero-content p{


font-size:1.05rem;

color:rgba(255,255,255,.8);

margin-bottom:25px;


}



.hero-actions{


display:flex;

gap:14px;


}



.hero-image{
    width:250px;
    height:250px;
    display:flex;
    align-items:center;
    justify-content:center;
}



.image-placeholder{
    width:220px;
    height:220px;
    border-radius:50%;
    background:rgba(255,255,255,.1);
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:5.5rem;
}



/* arrows */


.slider-prev,
.slider-next{


position:absolute;

top:50%;

transform:translateY(-50%);

border:none;

background:rgba(255,255,255,.15);

color:white;

width:45px;

height:45px;

border-radius:50%;

font-size:2rem;


}



.slider-prev{

right:25px;

}


.slider-next{

left:25px;

}



/* dots */


.slider-dots{


position:absolute;

bottom:20px;

left:50%;

transform:translateX(-50%);

display:flex;

gap:8px;


}


.slider-dots button{


width:10px;

height:10px;

border-radius:50%;

border:none;

background:white;

opacity:.4;


}



.slider-dots button.active{

opacity:1;

}




@media(max-width:800px){


.hero-container{

flex-direction:column;

text-align:center;

}



.hero-image{

width:220px;

height:220px;

}



.image-placeholder{

width:200px;

height:200px;

font-size:5rem;

}



.hero-content h1{

font-size:2rem;

}


}

</style>