package me.iacn.mbestyle.ui.fragment;

import android.app.Fragment;
import android.os.Bundle;
import android.support.annotation.IdRes;
import android.support.annotation.LayoutRes;
import android.support.annotation.Nullable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;

import me.iacn.mbestyle.R;

/**
 * Created by iAcn on 2017/2/20
 * Emali iAcn0301@foxmail.com
 */

public abstract class ILazyFragment extends Fragment {

    protected View mContentView;
    protected boolean mStartExecuted;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView();
    }

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        return View.inflate(getActivity(), getInitialView(), null);
    }

    @Override
    public void onActivityCreated(@Nullable Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);

        findView();
        setListener();
    }

    @Override
    public void setUserVisibleHint(boolean isVisibleToUser) {
        super.setUserVisibleHint(isVisibleToUser);

        if (isVisibleToUser && !isDataComplete() && mStartExecuted) {
            initData();
        }
    }

    @Override
    public void onStart() {
        super.onStart();

        if (getUserVisibleHint() && !isDataComplete()) {
            initData();
        }

        mStartExecuted = true;
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        mContentView = null;
    }

    @LayoutRes
    protected int getInitialView() {
        return R.layout.inflate_loading;
    }

    protected final void setContentView() {
        mContentView = View.inflate(getActivity(), getContentView(), null);
    }

    @LayoutRes
    protected abstract int getContentView();

    protected abstract void findView();

    protected abstract void setListener();

    protected abstract void initData();

    protected abstract boolean isDataComplete();

    protected final View findViewById(@IdRes int id) {
        return mContentView.findViewById(id);
    }

    public void onLoadData() {
        FrameLayout layout = (FrameLayout) getView();

        if (layout != null) {
            layout.removeAllViews();
            layout.addView(mContentView);
        }
    }
}