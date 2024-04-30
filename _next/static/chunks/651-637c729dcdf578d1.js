(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[651],{97498:function(e,t){"use strict";var n,r;Object.defineProperty(t,"__esModule",{value:!0}),function(e,t){for(var n in t)Object.defineProperty(e,n,{enumerable:!0,get:t[n]})}(t,{PrefetchKind:function(){return n},ACTION_REFRESH:function(){return o},ACTION_NAVIGATE:function(){return l},ACTION_RESTORE:function(){return u},ACTION_SERVER_PATCH:function(){return a},ACTION_PREFETCH:function(){return i},ACTION_FAST_REFRESH:function(){return c},ACTION_SERVER_ACTION:function(){return s}});let o="refresh",l="navigate",u="restore",a="server-patch",i="prefetch",c="fast-refresh",s="server-action";(r=n||(n={})).AUTO="auto",r.FULL="full",r.TEMPORARY="temporary",("function"==typeof t.default||"object"==typeof t.default&&null!==t.default)&&void 0===t.default.__esModule&&(Object.defineProperty(t.default,"__esModule",{value:!0}),Object.assign(t.default,t),e.exports=t.default)},10030:function(e,t,n){"use strict";function getDomainLocale(e,t,n,r){return!1}Object.defineProperty(t,"__esModule",{value:!0}),Object.defineProperty(t,"getDomainLocale",{enumerable:!0,get:function(){return getDomainLocale}}),n(22866),("function"==typeof t.default||"object"==typeof t.default&&null!==t.default)&&void 0===t.default.__esModule&&(Object.defineProperty(t.default,"__esModule",{value:!0}),Object.assign(t.default,t),e.exports=t.default)},65170:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),Object.defineProperty(t,"default",{enumerable:!0,get:function(){return y}});let r=n(38754),o=r._(n(67294)),l=n(74450),u=n(92227),a=n(64364),i=n(10109),c=n(73607),s=n(11823),f=n(89031),d=n(40920),p=n(10030),m=n(77192),h=n(97498),v=new Set;function prefetch(e,t,n,r,o,l){if(!l&&!(0,u.isLocalURL)(t))return;if(!r.bypassPrefetchedCheck){let o=void 0!==r.locale?r.locale:"locale"in e?e.locale:void 0,l=t+"%"+n+"%"+o;if(v.has(l))return;v.add(l)}let a=l?e.prefetch(t,o):e.prefetch(t,n,r);Promise.resolve(a).catch(e=>{})}function isModifiedEvent(e){let t=e.currentTarget,n=t.getAttribute("target");return n&&"_self"!==n||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey||e.nativeEvent&&2===e.nativeEvent.which}function linkClicked(e,t,n,r,l,a,i,c,s,f){let{nodeName:d}=e.currentTarget,p="A"===d.toUpperCase();if(p&&(isModifiedEvent(e)||!s&&!(0,u.isLocalURL)(n)))return;e.preventDefault();let navigate=()=>{let e=null==i||i;"beforePopState"in t?t[l?"replace":"push"](n,r,{shallow:a,locale:c,scroll:e}):t[l?"replace":"push"](r||n,{forceOptimisticNavigation:!f,scroll:e})};s?o.default.startTransition(navigate):navigate()}function formatStringOrUrl(e){return"string"==typeof e?e:(0,a.formatUrl)(e)}let g=o.default.forwardRef(function(e,t){let n,r;let{href:u,as:a,children:v,prefetch:g=null,passHref:y,replace:b,shallow:_,scroll:x,locale:j,onClick:C,onMouseEnter:O,onTouchStart:E,legacyBehavior:k=!1,...N}=e;n=v,k&&("string"==typeof n||"number"==typeof n)&&(n=o.default.createElement("a",null,n));let S=o.default.useContext(s.RouterContext),T=o.default.useContext(f.AppRouterContext),M=null!=S?S:T,R=!S,I=!1!==g,P=null===g?h.PrefetchKind.AUTO:h.PrefetchKind.FULL,{href:B,as:A}=o.default.useMemo(()=>{if(!S){let e=formatStringOrUrl(u);return{href:e,as:a?formatStringOrUrl(a):e}}let[e,t]=(0,l.resolveHref)(S,u,!0);return{href:e,as:a?(0,l.resolveHref)(S,a):t||e}},[S,u,a]),L=o.default.useRef(B),w=o.default.useRef(A);k&&(r=o.default.Children.only(n));let U=k?r&&"object"==typeof r&&r.ref:t,[D,q,H]=(0,d.useIntersection)({rootMargin:"200px"}),F=o.default.useCallback(e=>{(w.current!==A||L.current!==B)&&(H(),w.current=A,L.current=B),D(e),U&&("function"==typeof U?U(e):"object"==typeof U&&(U.current=e))},[A,U,B,H,D]);o.default.useEffect(()=>{M&&q&&I&&prefetch(M,B,A,{locale:j},{kind:P},R)},[A,B,q,j,I,null==S?void 0:S.locale,M,R,P]);let G={ref:F,onClick(e){k||"function"!=typeof C||C(e),k&&r.props&&"function"==typeof r.props.onClick&&r.props.onClick(e),M&&!e.defaultPrevented&&linkClicked(e,M,B,A,b,_,x,j,R,I)},onMouseEnter(e){k||"function"!=typeof O||O(e),k&&r.props&&"function"==typeof r.props.onMouseEnter&&r.props.onMouseEnter(e),M&&(I||!R)&&prefetch(M,B,A,{locale:j,priority:!0,bypassPrefetchedCheck:!0},{kind:P},R)},onTouchStart(e){k||"function"!=typeof E||E(e),k&&r.props&&"function"==typeof r.props.onTouchStart&&r.props.onTouchStart(e),M&&(I||!R)&&prefetch(M,B,A,{locale:j,priority:!0,bypassPrefetchedCheck:!0},{kind:P},R)}};if((0,i.isAbsoluteUrl)(A))G.href=A;else if(!k||y||"a"===r.type&&!("href"in r.props)){let e=void 0!==j?j:null==S?void 0:S.locale,t=(null==S?void 0:S.isLocaleDomain)&&(0,p.getDomainLocale)(A,e,null==S?void 0:S.locales,null==S?void 0:S.domainLocales);G.href=t||(0,m.addBasePath)((0,c.addLocale)(A,e,null==S?void 0:S.defaultLocale))}return k?o.default.cloneElement(r,G):o.default.createElement("a",{...N,...G},n)}),y=g;("function"==typeof t.default||"object"==typeof t.default&&null!==t.default)&&void 0===t.default.__esModule&&(Object.defineProperty(t.default,"__esModule",{value:!0}),Object.assign(t.default,t),e.exports=t.default)},40920:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),Object.defineProperty(t,"useIntersection",{enumerable:!0,get:function(){return useIntersection}});let r=n(67294),o=n(63436),l="function"==typeof IntersectionObserver,u=new Map,a=[];function createObserver(e){let t;let n={root:e.root||null,margin:e.rootMargin||""},r=a.find(e=>e.root===n.root&&e.margin===n.margin);if(r&&(t=u.get(r)))return t;let o=new Map,l=new IntersectionObserver(e=>{e.forEach(e=>{let t=o.get(e.target),n=e.isIntersecting||e.intersectionRatio>0;t&&n&&t(n)})},e);return t={id:n,observer:l,elements:o},a.push(n),u.set(n,t),t}function observe(e,t,n){let{id:r,observer:o,elements:l}=createObserver(n);return l.set(e,t),o.observe(e),function(){if(l.delete(e),o.unobserve(e),0===l.size){o.disconnect(),u.delete(r);let e=a.findIndex(e=>e.root===r.root&&e.margin===r.margin);e>-1&&a.splice(e,1)}}}function useIntersection(e){let{rootRef:t,rootMargin:n,disabled:u}=e,a=u||!l,[i,c]=(0,r.useState)(!1),s=(0,r.useRef)(null),f=(0,r.useCallback)(e=>{s.current=e},[]);(0,r.useEffect)(()=>{if(l){if(a||i)return;let e=s.current;if(e&&e.tagName){let r=observe(e,e=>e&&c(e),{root:null==t?void 0:t.current,rootMargin:n});return r}}else if(!i){let e=(0,o.requestIdleCallback)(()=>c(!0));return()=>(0,o.cancelIdleCallback)(e)}},[a,n,t,i,s.current]);let d=(0,r.useCallback)(()=>{c(!1)},[]);return[f,i,d]}("function"==typeof t.default||"object"==typeof t.default&&null!==t.default)&&void 0===t.default.__esModule&&(Object.defineProperty(t.default,"__esModule",{value:!0}),Object.assign(t.default,t),e.exports=t.default)},41664:function(e,t,n){e.exports=n(65170)},17215:function(e,t,n){"use strict";n.d(t,{D:function(){return r},i:function(){return o}});var[r,o]=(0,n(55227).k)({strict:!1,name:"ButtonGroupContext"})},96272:function(e,t,n){"use strict";n.d(t,{z:function(){return p}});var r=n(67294);function useButtonType(e){let[t,n]=(0,r.useState)(!e),o=(0,r.useCallback)(e=>{e&&n("BUTTON"===e.tagName)},[]);return{ref:o,type:t?"button":void 0}}var o=n(17215),l=n(51337),u=n(25432),a=n(85893);function ButtonIcon(e){let{children:t,className:n,...o}=e,i=(0,r.isValidElement)(t)?(0,r.cloneElement)(t,{"aria-hidden":!0,focusable:!1}):t,c=(0,u.cx)("chakra-button__icon",n);return(0,a.jsx)(l.m.span,{display:"inline-flex",alignSelf:"center",flexShrink:0,...o,className:c,children:i})}ButtonIcon.displayName="ButtonIcon";var i=n(295);function ButtonSpinner(e){let{label:t,placement:n,spacing:o="0.5rem",children:c=(0,a.jsx)(i.$,{color:"currentColor",width:"1em",height:"1em"}),className:s,__css:f,...d}=e,p=(0,u.cx)("chakra-button__spinner",s),m="start"===n?"marginEnd":"marginStart",h=(0,r.useMemo)(()=>({display:"flex",alignItems:"center",position:t?"relative":"absolute",[m]:t?o:0,fontSize:"1em",lineHeight:"normal",...f}),[f,t,m,o]);return(0,a.jsx)(l.m.div,{className:p,...d,__css:h,children:c})}ButtonSpinner.displayName="ButtonSpinner";var c=n(81103),s=n(35059),f=n(54662),d=n(33179),p=(0,s.G)((e,t)=>{let n=(0,o.i)(),i=(0,f.mq)("Button",{...n,...e}),{isDisabled:s=null==n?void 0:n.isDisabled,isLoading:p,isActive:m,children:h,leftIcon:v,rightIcon:g,loadingText:y,iconSpacing:b="0.5rem",type:_,spinner:x,spinnerPlacement:j="start",className:C,as:O,...E}=(0,d.Lr)(e),k=(0,r.useMemo)(()=>{let e={...null==i?void 0:i._focus,zIndex:1};return{display:"inline-flex",appearance:"none",alignItems:"center",justifyContent:"center",userSelect:"none",position:"relative",whiteSpace:"nowrap",verticalAlign:"middle",outline:"none",...i,...!!n&&{_focus:e}}},[i,n]),{ref:N,type:S}=useButtonType(O),T={rightIcon:g,leftIcon:v,iconSpacing:b,children:h};return(0,a.jsxs)(l.m.button,{ref:(0,c.qq)(t,N),as:O,type:null!=_?_:S,"data-active":(0,u.PB)(m),"data-loading":(0,u.PB)(p),__css:k,className:(0,u.cx)("chakra-button",C),...E,disabled:s||p,children:[p&&"start"===j&&(0,a.jsx)(ButtonSpinner,{className:"chakra-button__spinner--start",label:y,placement:"start",spacing:b,children:x}),p?y||(0,a.jsx)(l.m.span,{opacity:0,children:(0,a.jsx)(ButtonContent,{...T})}):(0,a.jsx)(ButtonContent,{...T}),p&&"end"===j&&(0,a.jsx)(ButtonSpinner,{className:"chakra-button__spinner--end",label:y,placement:"end",spacing:b,children:x})]})});function ButtonContent(e){let{leftIcon:t,rightIcon:n,children:r,iconSpacing:o}=e;return(0,a.jsxs)(a.Fragment,{children:[t&&(0,a.jsx)(ButtonIcon,{marginEnd:o,children:t}),r,n&&(0,a.jsx)(ButtonIcon,{marginStart:o,children:n})]})}p.displayName="Button"},14418:function(e,t,n){"use strict";n.d(t,{X:function(){return c}});var r=n(35059),o=n(54662),l=n(33179),u=n(51337),a=n(25432),i=n(85893),c=(0,r.G)(function(e,t){let n=(0,o.mq)("Heading",e),{className:r,...c}=(0,l.Lr)(e);return(0,i.jsx)(u.m.h2,{ref:t,className:(0,a.cx)("chakra-heading",e.className),...c,__css:n})});c.displayName="Heading"},204:function(e,t,n){"use strict";n.d(t,{k:function(){return u}});var r=n(35059),o=n(51337),l=n(85893),u=(0,r.G)(function(e,t){let{direction:n,align:r,justify:u,wrap:a,basis:i,grow:c,shrink:s,...f}=e;return(0,l.jsx)(o.m.div,{ref:t,__css:{display:"flex",flexDirection:n,alignItems:r,justifyContent:u,flexWrap:a,flexBasis:i,flexGrow:c,flexShrink:s},...f})});u.displayName="Flex"},9564:function(e,t,n){"use strict";n.d(t,{x:function(){return c}});var r=n(35059),o=n(54662),l=n(33179),u=n(51337),a=n(25432);function compact(e){let t=Object.assign({},e);for(let e in t)void 0===t[e]&&delete t[e];return t}var i=n(85893),c=(0,r.G)(function(e,t){let n=(0,o.mq)("Text",e),{className:r,align:c,decoration:s,casing:f,...d}=(0,l.Lr)(e),p=compact({textAlign:e.align,textDecoration:e.decoration,textTransform:e.casing});return(0,i.jsx)(u.m.p,{ref:t,className:(0,a.cx)("chakra-text",e.className),...p,...d,__css:n})});c.displayName="Text"},81103:function(e,t,n){"use strict";n.d(t,{lq:function(){return mergeRefs},qq:function(){return useMergeRefs}});var r=n(67294);function assignRef(e,t){if(null!=e){if("function"==typeof e){e(t);return}try{e.current=t}catch(n){throw Error(`Cannot assign value '${t}' to ref '${e}'`)}}}function mergeRefs(...e){return t=>{e.forEach(e=>{assignRef(e,t)})}}function useMergeRefs(...e){return(0,r.useMemo)(()=>mergeRefs(...e),e)}}}]);