var Slider = React.createClass({
    getInitialState: function(){
        return {data:[
            {
                image:"http://lorempixel.com/580/250/nature/1",
                align:"center",
                title:"This is our big Tagline!",
                slogan:"Here's our small slogan."
            },{
                image:"http://lorempixel.com/580/250/nature/2",
                align:"left",
                title:"Left Aligned Caption",
                slogan:"Here's our small slogan."
            },{
                image:"http://lorempixel.com/580/250/nature/3",
                align:"right",
                title:"Right Aligned Caption",
                slogan:"Here's our small slogan."
            },{
                image:"http://lorempixel.com/580/250/nature/4",
                align:"center",
                title:"<i>This is our big Taglineb!</i>",
                slogan:"Here's our small slogan."
            }
        ]}
    },
    render: function(){
        var slides = this.state.data.map(function(slide, index){
            return (
                <Slide image={slide.image} align={slide.align} title={slide.title} slogan={slide.slogan} key={index}>
                </Slide>
            )
        });
        return (
            <ul className="slides">
                {slides}
            </ul>
        );
    }
});
var Slide = React.createClass({
    render: function () {
        return (
            <li>
                <img src={this.props.image}/>
                <div className={"caption "+this.props.align+"-align"}>
                    <h3>{this.props.title}</h3>
                    <h5 className="light grey-text text-lighten-3">{this.props.slogan}</h5>
                </div>
            </li>
        );
    }
});
React.render(<Slider/>,document.getElementById('slider'));
$(document).ready(function(){$('.slider').slider();});