import { useCookies } from "vue3-cookies";

const _key= 'SIGNER-AUTH';
const _regex = /^auth\-key\-[a-z0-9]{32}$/
const _expires = new Date(0).toUTCString();

const { cookies } = useCookies();

const getCookie = () => {
    return cookies.get(_key)?.match(_regex)?.at(0);
};

const checkCookie = () => {
    return !!getCookie();
};

const clearCookie = () => {
    return cookies.remove(_key);
};

export {getCookie, checkCookie, clearCookie};