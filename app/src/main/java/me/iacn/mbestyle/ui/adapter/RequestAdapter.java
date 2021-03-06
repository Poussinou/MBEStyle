package me.iacn.mbestyle.ui.adapter;

import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CheckBox;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.List;

import me.iacn.mbestyle.R;
import me.iacn.mbestyle.bean.RequestBean;
import me.iacn.mbestyle.presenter.RequestPresenter;
import me.iacn.mbestyle.ui.callback.OnItemClickListener;
import me.iacn.mbestyle.ui.callback.OnItemLongClickListener;

/**
 * Created by iAcn on 2017/2/19
 * Email i@iacn.me
 */

public class RequestAdapter extends RecyclerView.Adapter<RequestHolder> {

    private List<RequestBean> mApps;
    private RequestPresenter mPresenter;
    private OnItemClickListener mClickListener;
    private OnItemLongClickListener mLongListener;

    public RequestAdapter(List<RequestBean> mApps, RequestPresenter presenter) {
        this.mApps = mApps;
        this.mPresenter = presenter;
    }

    @Override
    public RequestHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        RequestHolder holder = new RequestHolder(LayoutInflater.from(
                parent.getContext()).inflate(R.layout.item_request, parent, false));
        holder.mClickListener = mClickListener;
        holder.mLongListener = mLongListener;

        return holder;
    }

    @Override
    public void onBindViewHolder(RequestHolder holder, int position) {
        RequestBean bean = mApps.get(position);

        holder.ivIcon.setImageDrawable(bean.icon);
        holder.tvName.setText(bean.name);
        holder.cbCheck.setChecked(bean.isCheck);

        mPresenter.getRequestTotal(bean.packageName, bean, holder.tvTotal);
    }

    @Override
    public int getItemCount() {
        return mApps.size();
    }

    public void setOnItemClickListener(OnItemClickListener listener) {
        mClickListener = listener;
    }

    public void setOnItemLongClickListener(OnItemLongClickListener listener) {
        mLongListener = listener;
    }
}

class RequestHolder extends RecyclerView.ViewHolder implements View.OnClickListener, View.OnLongClickListener {

    OnItemClickListener mClickListener;
    OnItemLongClickListener mLongListener;

    ImageView ivIcon;
    TextView tvName;
    TextView tvTotal;
    CheckBox cbCheck;

    RequestHolder(View itemView) {
        super(itemView);

        ivIcon = (ImageView) itemView.findViewById(R.id.iv_icon);
        tvName = (TextView) itemView.findViewById(R.id.tv_name);
        tvTotal = (TextView) itemView.findViewById(R.id.tv_total);
        cbCheck = (CheckBox) itemView.findViewById(R.id.cb_check);

        itemView.setOnClickListener(this);
        itemView.setOnLongClickListener(this);
    }

    @Override
    public void onClick(View v) {
        if (mClickListener != null) {
            mClickListener.onItemClick(v, getLayoutPosition());
        }
    }

    @Override
    public boolean onLongClick(View v) {
        return mLongListener != null && mLongListener.onItemLongClick(v, getLayoutPosition());
    }
}