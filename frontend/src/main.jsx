import React,{useEffect,useState} from 'react';
import {createRoot} from 'react-dom/client';
import './style.css';
const API=import.meta.env.VITE_API_URL||'http://localhost:8000';
function App(){
 const [products,setProducts]=useState([]),[cart,setCart]=useState([]),[dash,setDash]=useState({});
 const load=()=>Promise.all([fetch(API+'/api/products').then(r=>r.json()).then(setProducts),fetch(API+'/api/dashboard').then(r=>r.json()).then(setDash)]);
 useEffect(()=>{load()},[]);
 const add=p=>setCart(c=>[...c.filter(x=>x.id!==p.id),{...p,qty:(c.find(x=>x.id===p.id)?.qty||0)+1}]);
 const checkout=async()=>{const r=await fetch(API+'/api/checkout',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items:cart.map(x=>({product_id:x.id,quantity:x.qty}))})}); if(r.ok){setCart([]);load();alert('Sale completed: $'+(await r.json()).total)}else alert((await r.json()).detail)};
 return <main><header><div><h1>RetailForge</h1><p>Supermarket POS</p></div><div className="metrics"><span>Sales {dash.sales_count||0}</span><span>Revenue ${Number(dash.revenue||0).toFixed(2)}</span><span>Low stock {dash.low_stock_items||0}</span></div></header>
 <section><div><h2>Products</h2><div className="grid">{products.map(p=><button className="card" key={p.id} onClick={()=>add(p)}><b>{p.name}</b><span>{p.category}</span><strong>${p.price.toFixed(2)}</strong><small>Stock {p.stock}</small></button>)}</div></div>
 <aside><h2>Cart</h2>{cart.map(x=><div className="line" key={x.id}><span>{x.name} × {x.qty}</span><b>${(x.price*x.qty).toFixed(2)}</b></div>)}<hr/><button className="checkout" disabled={!cart.length} onClick={checkout}>Checkout</button></aside></section></main>
}
createRoot(document.getElementById('root')).render(<App/>);